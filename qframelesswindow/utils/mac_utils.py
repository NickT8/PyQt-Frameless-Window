# coding:utf-8
from ctypes import c_void_p

import Cocoa
import objc
from PySide6.QtCore import qVersion
from PySide6.QtWidgets import QWidget
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent,
    kCGEventLeftMouseDown,
    kCGMouseButtonLeft,
)

QT_VERSION = tuple(int(v) for v in qVersion().split("."))


class MacMoveResize:
    """Tool class for moving and resizing Mac OS window"""

    @staticmethod
    def start_system_move(window: QWidget, globalPos):
        """resize window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event
        """
        if QT_VERSION >= (5, 15, 0):
            window.window_handle().start_system_move()
            return

        nsWindow = get_ns_window(window.win_id())

        # send click event
        cgEvent = CGEventCreateMouseEvent(
            None, kCGEventLeftMouseDown, (globalPos.x(), globalPos.y()), kCGMouseButtonLeft
        )
        clickEvent = Cocoa.NSEvent.eventWithCGEvent_(cgEvent)

        if clickEvent:
            nsWindow.performWindowDragWithEvent_(clickEvent)

        # CFRelease(cgEvent)

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
        pass


def get_ns_window(win_id):
    """convert window handle to NSWindow

    Parameters
    ----------
    win_id: int or `sip.voidptr`
        window handle
    """
    view = objc.objc_object(c_void_p=c_void_p(int(win_id)))
    return view.window()
