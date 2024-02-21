# coding:utf-8
from enum import Enum

from PySide6.QtCore import Property, QFile, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QAbstractButton
from PySide6.QtXml import QDomDocument

from __feature__ import snake_case  # isort: skip  # noqa: F401

from .._rc import resource  # noqa: F401


class TitleBarButtonState(Enum):
    """Title bar button state"""

    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class TitleBarButton(QAbstractButton):
    """Title bar button"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_cursor(Qt.ArrowCursor)
        self.set_fixed_size(46, 32)
        self._state = TitleBarButtonState.NORMAL

        # icon color
        self._normal_color = QColor(0, 0, 0)
        self._hover_color = QColor(0, 0, 0)
        self._pressed_color = QColor(0, 0, 0)

        # background color
        self._normal_bg_color = QColor(0, 0, 0, 0)
        self._hover_bg_color = QColor(0, 0, 0, 26)
        self._pressed_bg_color = QColor(0, 0, 0, 51)

    def set_state(self, state):
        """set the state of button

        Parameters
        ----------
        state: TitleBarButtonState
            the state of button
        """
        self._state = state
        self.update()

    def is_pressed(self):
        """whether the button is pressed"""
        return self._state == TitleBarButtonState.PRESSED

    def get_normal_color(self):
        """get the icon color of the button in normal state"""
        return self._normal_color

    def get_hover_color(self):
        """get the icon color of the button in hover state"""
        return self._hover_color

    def get_pressed_color(self):
        """get the icon color of the button in pressed state"""
        return self._pressed_color

    def get_normal_background_color(self):
        """get the background color of the button in normal state"""
        return self._normal_bg_color

    def get_hover_background_color(self):
        """get the background color of the button in hover state"""
        return self._hover_bg_color

    def get_pressed_background_color(self):
        """get the background color of the button in pressed state"""
        return self._pressed_bg_color

    def set_normal_color(self, color):
        """set the icon color of the button in normal state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._normal_color = QColor(color)
        self.update()

    def set_hover_color(self, color):
        """set the icon color of the button in hover state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._hover_color = QColor(color)
        self.update()

    def set_pressed_color(self, color):
        """set the icon color of the button in pressed state

        Parameters
        ----------
        color: QColor
            icon color
        """
        self._pressed_color = QColor(color)
        self.update()

    def set_normal_background_color(self, color):
        """set the background color of the button in normal state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._normal_bg_color = QColor(color)
        self.update()

    def set_hover_background_color(self, color):
        """set the background color of the button in hover state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._hover_bg_color = QColor(color)
        self.update()

    def set_pressed_background_color(self, color):
        """set the background color of the button in pressed state

        Parameters
        ----------
        color: QColor
            background color
        """
        self._pressed_bg_color = QColor(color)
        self.update()

    def enter_event(self, e):
        self.set_state(TitleBarButtonState.HOVER)
        super().enter_event(e)

    def leave_event(self, e):
        self.set_state(TitleBarButtonState.NORMAL)
        super().leave_event(e)

    def mouse_press_event(self, e):
        if e.button() != Qt.LeftButton:
            return

        self.set_state(TitleBarButtonState.PRESSED)
        super().mouse_press_event(e)

    def _get_colors(self):
        """get the icon color and background color"""
        if self._state == TitleBarButtonState.NORMAL:
            return self._normal_color, self._normal_bg_color
        elif self._state == TitleBarButtonState.HOVER:
            return self._hover_color, self._hover_bg_color

        return self._pressed_color, self._pressed_bg_color

    normal_color = Property(QColor, get_normal_color, set_normal_color)
    hover_color = Property(QColor, get_hover_color, set_hover_color)
    pressed_color = Property(QColor, get_pressed_color, set_pressed_color)
    normal_background_color = Property(
        QColor, get_normal_background_color, set_normal_background_color
    )
    hover_background_color = Property(
        QColor, get_hover_background_color, set_hover_background_color
    )
    pressed_background_color = Property(
        QColor, get_pressed_background_color, set_pressed_background_color
    )


class SvgTitleBarButton(TitleBarButton):
    """Title bar button using svg icon"""

    def __init__(self, iconPath, parent=None):
        """
        Parameters
        ----------
        iconPath: str
            the path of icon

        parent: QWidget
            parent widget
        """
        super().__init__(parent)
        self._svg_dom = QDomDocument()
        self.set_icon(iconPath)

    def set_icon(self, iconPath):
        """set the icon of button

        Parameters
        ----------
        iconPath: str
            the path of icon
        """
        f = QFile(iconPath)
        f.open(QFile.ReadOnly)
        self._svg_dom.set_content(f.read_all())
        f.close()

    def paint_event(self, e):
        painter = QPainter(self)
        painter.set_render_hints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        color, bgColor = self._get_colors()

        # draw background
        painter.set_brush(bgColor)
        painter.set_pen(Qt.NoPen)
        painter.draw_rect(self.rect())

        # draw icon
        color = color.name()
        pathNodes = self._svg_dom.elements_by_tag_name("path")
        for i in range(pathNodes.length()):
            element = pathNodes.at(i).to_element()
            element.set_attribute("stroke", color)

        renderer = QSvgRenderer(self._svg_dom.to_byte_array())
        renderer.render(painter, QRectF(self.rect()))


class MinimizeButton(TitleBarButton):
    """Minimize button"""

    def paint_event(self, e):
        painter = QPainter(self)
        color, bgColor = self._get_colors()

        # draw background
        painter.set_brush(bgColor)
        painter.set_pen(Qt.NoPen)
        painter.draw_rect(self.rect())

        # draw icon
        painter.set_brush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.set_cosmetic(True)
        painter.set_pen(pen)
        painter.draw_line(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    """Maximize button"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isMax = False

    def set_max_state(self, isMax):
        """update the maximized state and icon"""
        if self._isMax == isMax:
            return

        self._isMax = isMax
        self.set_state(TitleBarButtonState.NORMAL)

    def paint_event(self, e):
        painter = QPainter(self)
        color, bgColor = self._get_colors()

        # draw background
        painter.set_brush(bgColor)
        painter.set_pen(Qt.NoPen)
        painter.draw_rect(self.rect())

        # draw icon
        painter.set_brush(Qt.NoBrush)
        pen = QPen(color, 1)
        pen.set_cosmetic(True)
        painter.set_pen(pen)

        r = self.device_pixel_ratio_f()
        painter.scale(1 / r, 1 / r)
        if not self._isMax:
            painter.draw_rect(int(18 * r), int(11 * r), int(10 * r), int(10 * r))
        else:
            painter.draw_rect(int(18 * r), int(13 * r), int(8 * r), int(8 * r))
            x0 = int(18 * r) + int(2 * r)
            y0 = 13 * r
            dw = int(2 * r)
            path = QPainterPath(QPointF(x0, y0))
            path.line_to(x0, y0 - dw)
            path.line_to(x0 + 8 * r, y0 - dw)
            path.line_to(x0 + 8 * r, y0 - dw + 8 * r)
            path.line_to(x0 + 8 * r - dw, y0 - dw + 8 * r)
            painter.draw_path(path)


class CloseButton(SvgTitleBarButton):
    """Close button"""

    def __init__(self, parent=None):
        super().__init__(":/qframelesswindow/close.svg", parent)
        self.set_hover_color(Qt.white)
        self.set_pressed_color(Qt.white)
        self.set_hover_background_color(QColor(232, 17, 35))
        self.set_pressed_background_color(QColor(241, 112, 122))
