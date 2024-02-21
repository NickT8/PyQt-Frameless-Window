# coding:utf-8
import Cocoa
import objc
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QDialog, QMainWindow, QWidget

from ..titlebar import TitleBar
from .window_effect import MacWindowEffect


class MacFramelessWindowBase:
    """Frameless window base class for mac"""

    def __init__(self, *args, **kwargs):
        pass

    def _init_frameless(self):
        self.window_effect = MacWindowEffect(self)
        # must enable acrylic effect before creating title bar
        if isinstance(self, AcrylicWindow):
            self.window_effect.set_acrylic_effect(self.win_id())

        self.title_bar = TitleBar(self)
        self._is_resize_enabled = True

        self.update_frameless()

        self.resize(500, 500)
        self.title_bar.raise_()

    def update_frameless(self):
        view = objc.objc_object(c_void_p=self.win_id().__int__())
        self.__ns_window = view.window()

        # hide system title bar
        self._hide_system_title_bar()

    def set_title_bar(self, titleBar):
        """set custom title bar

        Parameters
        ----------
        titleBar: TitleBar
            title bar
        """
        self.title_bar.deleteLater()
        self.title_bar.hide()
        self.title_bar = titleBar
        self.title_bar.setParent(self)
        self.title_bar.raise_()

    def set_resize_enabled(self, isEnabled: bool):
        """set whether resizing is enabled"""
        self._is_resize_enabled = isEnabled

    def resize_event(self, e):
        self.title_bar.resize(self.width(), self.title_bar.height())

    def change_event(self, event):
        if event.type() == QEvent.WindowStateChange:
            self._hide_system_title_bar()

    def _hide_system_title_bar(self):
        # extend view to title bar region
        self.__ns_window.setStyleMask_(
            self.__ns_window.styleMask() | Cocoa.NSFullSizeContentViewWindowMask
        )
        self.__ns_window.setTitlebarAppearsTransparent_(True)

        # disable the moving behavior of system
        self.__ns_window.setMovableByWindowBackground_(False)
        self.__ns_window.setMovable_(False)

        # hide title bar buttons and title
        self.__ns_window.setShowsToolbarButton_(False)
        self.__ns_window.setTitleVisibility_(Cocoa.NSWindowTitleHidden)
        self.__ns_window.standardWindowButton_(Cocoa.NSWindowCloseButton).setHidden_(True)
        self.__ns_window.standardWindowButton_(Cocoa.NSWindowZoomButton).setHidden_(True)
        self.__ns_window.standardWindowButton_(Cocoa.NSWindowMiniaturizeButton).setHidden_(True)


class MacFramelessWindow(QWidget, MacFramelessWindowBase):
    """Frameless window for Linux system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()

    def resize_event(self, e):
        MacFramelessWindowBase.resize_event(self, e)

    def change_event(self, e):
        MacFramelessWindowBase.change_event(self, e)

    def paint_event(self, e):
        QWidget.paint_event(self, e)
        self._hide_system_title_bar()


class AcrylicWindow(MacFramelessWindow):
    """A frameless window with acrylic effect"""

    def _init_frameless(self):
        super()._init_frameless()
        self.set_attribute(Qt.WA_TranslucentBackground)
        self.window_effect.set_acrylic_effect(self.win_id())
        self.set_style_sheet("background: transparent")


class MacFramelessMainWindow(QMainWindow, MacFramelessWindowBase):
    """Frameless window for Linux system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()

    def resize_event(self, e):
        QMainWindow.resize_event(self, e)
        MacFramelessWindowBase.resize_event(self, e)

    def change_event(self, e):
        MacFramelessWindowBase.change_event(self, e)

    def paint_event(self, e):
        QMainWindow.paint_event(self, e)
        self._hide_system_title_bar()


class MacFramelessDialog(QDialog, MacFramelessWindowBase):
    """Frameless window for Linux system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()
        self.title_bar.min_btn.hide()
        self.title_bar.max_btn.hide()
        self.title_bar.set_double_click_enabled(False)

    def resize_event(self, e):
        MacFramelessWindowBase.resize_event(self, e)

    def change_event(self, e):
        MacFramelessWindowBase.change_event(self, e)

    def paint_event(self, e):
        QDialog.paint_event(self, e)
        self._hide_system_title_bar()
