# coding:utf-8
import sys

if sys.platform == "win32":
    from .win32_utils import WindowsMoveResize as MoveResize
elif sys.platform == "darwin":
    from .mac_utils import MacMoveResize as MoveResize
else:
    from .linux_utils import LinuxMoveResize as MoveResize


def start_system_move(window, globalPos):
    """resize window

    Parameters
    ----------
    window: QWidget
        window

    globalPos: QPoint
        the global point of mouse release event
    """
    MoveResize.start_system_move(window, globalPos)


def star_system_resize(window, globalPos, edges):
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
    MoveResize.star_system_resize(window, globalPos, edges)
