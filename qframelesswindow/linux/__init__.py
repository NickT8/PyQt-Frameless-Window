# coding:utf-8
from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtWidgets import QDialog, QMainWindow, QWidget

from ..titlebar import TitleBar
from ..utils.linux_utils import LinuxMoveResize
from .window_effect import LinuxWindowEffect


class LinuxFramelessWindowBase:
    """Frameless window base class for Linux system"""

    BORDER_WIDTH = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _init_frameless(self):
        self.window_effect = LinuxWindowEffect(self)
        self.title_bar = TitleBar(self)
        self._is_resize_enabled = True

        self.update_frameless()
        QCoreApplication.instance().install_event_filter(self)

        self.title_bar.raise_()
        self.resize(500, 500)

    def update_frameless(self):
        self.set_window_flags(self.window_flags() | Qt.FramelessWindowHint)

    def resize_event(self, e):
        self.title_bar.resize(self.width(), self.title_bar.height())

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

    def set_resize_enabled(self, is_enabled: bool):
        """set whether resizing is enabled"""
        self._is_resize_enabled = is_enabled

    def event_filter(self, obj, event):
        et = event.type()
        if et != QEvent.MouseButtonPress and et != QEvent.MouseMove or not self._is_resize_enabled:
            return False

        edges = Qt.Edge(0)
        pos = event.global_pos() - self.pos()
        if pos.x() < self.BORDER_WIDTH:
            edges |= Qt.LeftEdge
        if pos.x() >= self.width() - self.BORDER_WIDTH:
            edges |= Qt.RightEdge
        if pos.y() < self.BORDER_WIDTH:
            edges |= Qt.TopEdge
        if pos.y() >= self.height() - self.BORDER_WIDTH:
            edges |= Qt.BottomEdge

        # change cursor
        if et == QEvent.MouseMove and self.window_state() == Qt.WindowNoState:
            if edges in (Qt.LeftEdge | Qt.TopEdge, Qt.RightEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeFDiagCursor)
            elif edges in (Qt.RightEdge | Qt.TopEdge, Qt.LeftEdge | Qt.BottomEdge):
                self.setCursor(Qt.SizeBDiagCursor)
            elif edges in (Qt.TopEdge, Qt.BottomEdge):
                self.setCursor(Qt.SizeVerCursor)
            elif edges in (Qt.LeftEdge, Qt.RightEdge):
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

        elif obj in (self, self.title_bar) and et == QEvent.MouseButtonPress and edges:
            LinuxMoveResize.star_system_resize(self, event.global_pos(), edges)

        return False


class LinuxFramelessWindow(LinuxFramelessWindowBase, QWidget):
    """Frameless window for Linux system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()


class LinuxFramelessMainWindow(LinuxFramelessWindowBase, QMainWindow):
    """Frameless main window for Linux system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()


class LinuxFramelessDialog(LinuxFramelessWindowBase, QDialog):
    """Frameless dialog for Windows system"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_frameless()
        self.title_bar.min_btn.hide()
        self.title_bar.max_btn.hide()
        self.title_bar.set_double_click_enabled(False)
