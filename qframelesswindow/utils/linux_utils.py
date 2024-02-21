# coding: utf-8
from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication


class LinuxMoveResize:
    """Tool class for moving and resizing window"""

    @classmethod
    def start_system_move(cls, window, globalPos):
        """move window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event
        """
        window.window_handle().start_system_move()
        event = QMouseEvent(
            QEvent.MouseButtonRelease, QPoint(-1, -1), Qt.LeftButton, Qt.NoButton, Qt.NoModifier
        )
        QApplication.instance().post_event(window.window_handle(), event)

    @classmethod
    def star_system_resize(cls, window, globalPos, edges):
        """resize window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event

        edges: `Qt.Edges`
            window edges
        """
        if not edges:
            return

        window.window_handle().start_system_resize(edges)
