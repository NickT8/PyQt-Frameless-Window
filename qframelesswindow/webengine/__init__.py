# coding: utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView

from qframelesswindow import (
    AcrylicWindow,
    FramelessDialog,
    FramelessMainWindow,
    FramelessWindow,
)

from __feature__ import snake_case  # isort: skip  # noqa: F401


class FramelessWebEngineView(QWebEngineView):
    """Frameless web engine view"""

    def __init__(self, parent):
        if sys.platform == "win32" and isinstance(parent.window(), AcrylicWindow):
            parent.window().set_attribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        super().__init__(parent=parent)
        self.set_html("")

        if isinstance(self.window(), (FramelessWindow, FramelessMainWindow, FramelessDialog)):
            self.window().update_frameless()
