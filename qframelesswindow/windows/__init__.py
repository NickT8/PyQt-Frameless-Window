# coding:utf-8
from ctypes import cast
from ctypes.wintypes import LPRECT, MSG

import win32con
import win32gui
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QCursor
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QWidget

from ..titlebar import TitleBar
from ..utils import win32_utils as win_utils
from ..utils.win32_utils import Taskbar
from .c_structures import LPNCCALCSIZE_PARAMS
from .window_effect import WindowsWindowEffect

from __feature__ import snake_case  # isort: skip  # noqa: F401


class WindowsFramelessWindowBase:
    """Frameless window base class for Windows system"""

    BORDER_WIDTH = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _init_frameless(self):
        self.window_effect = WindowsWindowEffect(self)
        self.title_bar = TitleBar(self)
        self._is_resize_enabled = True

        self.update_frameless()

        # solve issue #5
        self.window_handle().screenChanged.connect(self.__on_screen_changed)

        self.resize(500, 500)
        self.title_bar.raise_()

    def update_frameless(self):
        """update frameless window"""
        self.set_window_flags(self.window_flags() | Qt.FramelessWindowHint)

        # add DWM shadow and window animation
        self.window_effect.add_window_animation(self.win_id())
        if not isinstance(self, AcrylicWindow):
            self.window_effect.add_shadow_effect(self.win_id())

    def set_title_bar(self, titleBar):
        """set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.title_bar.delete_later()
        self.title_bar.hide()
        self.title_bar = titleBar
        self.title_bar.set_parent(self)
        self.title_bar.raise_()

    def set_resize_enabled(self, isEnabled: bool):
        """set whether resizing is enabled"""
        self._is_resize_enabled = isEnabled

    def native_event(self, event_type, message):
        """Handle the Windows message"""
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return False, 0

        if msg.message == win32con.WM_NCHITTEST and self._is_resize_enabled:
            pos = QCursor.pos()
            x_pos = pos.x() - self.x()
            y_pos = pos.y() - self.y()
            w = self.frame_geometry().width()
            h = self.frame_geometry().height()

            # fixes https://github.com/zhiyiYo/PyQt-Frameless-Window/issues/98
            bw = (
                0
                if win_utils.is_maximized(msg.hWnd) or win_utils.is_full_screen(msg.hWnd)
                else self.BORDER_WIDTH
            )
            lx = x_pos < bw
            rx = x_pos > w - bw
            ty = y_pos < bw
            by = y_pos > h - bw
            if lx and ty:
                return True, win32con.HTTOPLEFT
            elif rx and by:
                return True, win32con.HTBOTTOMRIGHT
            elif rx and ty:
                return True, win32con.HTTOPRIGHT
            elif lx and by:
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
            else:
                rect = cast(msg.lParam, LPRECT).contents

            isMax = win_utils.is_maximized(msg.hWnd)
            isFull = win_utils.is_full_screen(msg.hWnd)

            # adjust the size of client rect
            if isMax and not isFull:
                ty = win_utils.get_resize_border_thickness(msg.hWnd, False)
                rect.top += ty
                rect.bottom -= ty

                tx = win_utils.get_resize_border_thickness(msg.hWnd, True)
                rect.left += tx
                rect.right -= tx

            # handle the situation that an auto-hide taskbar is enabled
            if (isMax or isFull) and Taskbar.is_auto_hide():
                position = Taskbar.get_position(msg.hWnd)
                if position == Taskbar.LEFT:
                    rect.top += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.BOTTOM:
                    rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.LEFT:
                    rect.left += Taskbar.AUTO_HIDE_THICKNESS
                elif position == Taskbar.RIGHT:
                    rect.right -= Taskbar.AUTO_HIDE_THICKNESS

            result = 0 if not msg.wParam else win32con.WVR_REDRAW
            return True, result

        return False, 0

    def __on_screen_changed(self):
        hWnd = int(self.window_handle().win_id())
        win32gui.SetWindowPos(
            hWnd,
            None,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED,
        )

    def resize_event(self, e):
        self.title_bar.resize(self.width(), self.title_bar.height())


class WindowsFramelessWindow(WindowsFramelessWindowBase, QWidget):
    """Frameless window for Windows system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()


class AcrylicWindow(WindowsFramelessWindow):
    """A frameless window with acrylic effect"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__closedByKey = False

    def _init_frameless(self):
        super()._init_frameless()
        self.update_frameless()

        self.set_style_sheet("AcrylicWindow{background:transparent}")

    def update_frameless(self):
        self.set_window_flags(Qt.FramelessWindowHint)

        self.window_effect.enable_blur_behind_window(self.win_id())
        self.window_effect.add_window_animation(self.win_id())

        self.window_effect.set_acrylic_effect(self.win_id())
        if win_utils.is_greater_equal_win11():
            self.window_effect.add_shadow_effect(self.win_id())

    def native_event(self, eventType, message):
        """Handle the Windows message"""
        msg = MSG.from_address(message.__int__())

        # handle Alt+F4
        if msg.message == win32con.WM_SYSKEYDOWN:
            if msg.wParam == win32con.VK_F4:
                self.__closedByKey = True
                QApplication.send_event(self, QCloseEvent())
                return False, 0

        return super().native_event(eventType, message)

    def closeEvent(self, e):
        if not self.__closedByKey or QApplication.quit_on_last_window_closed():
            self.__closedByKey = False
            return super().close_event(e)

        # system tray icon
        self.__closedByKey = False
        self.hide()


class WindowsFramelessMainWindow(WindowsFramelessWindowBase, QMainWindow):
    """Frameless main window for Windows system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()


class WindowsFramelessDialog(WindowsFramelessWindowBase, QDialog):
    """Frameless dialog for Windows system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()
        self.title_bar.min_btn.hide()
        self.title_bar.max_btn.hide()
        self.title_bar.set_double_click_enabled(False)
        self.window_effect.disable_maximize_button(self.win_id())
