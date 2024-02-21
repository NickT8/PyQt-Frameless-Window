# coding:utf-8

import sys

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from ..utils import startSystemMove
from .title_bar_buttons import (
    CloseButton,
    MaximizeButton,
    MinimizeButton,
    SvgTitleBarButton,  # noqa: F401
    TitleBarButton,
)

from __feature__ import snake_case  # isort: skip  # noqa: F401


class TitleBarBase(QWidget):
    """Title bar base class"""

    def __init__(self, parent):
        super().__init__(parent)
        self.min_btn = MinimizeButton(parent=self)
        self.close_btn = CloseButton(parent=self)
        self.max_btn = MaximizeButton(parent=self)

        self._is_double_click_enabled = True

        self.resize(200, 32)
        self.set_fixed_height(32)

        # connect signal to slot
        self.min_btn.clicked.connect(self.window().show_minimized)
        self.max_btn.clicked.connect(self.__toggle_max_state)
        self.close_btn.clicked.connect(self.window().close)

        self.window().install_event_filter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.WindowStateChange:
                self.max_btn.setMaxState(self.window().is_maximized())
                return False

        return super().event_filter(obj, e)

    def mouse_double_click_event(self, event):
        """Toggles the maximization state of the window"""
        if event.button() != Qt.LeftButton or not self._is_double_click_enabled:
            return

        self.__toggle_max_state()

    def mouse_move_event(self, e):
        if sys.platform != "win32" or not self.can_drag(e.pos()):
            return

        startSystemMove(self.window(), e.global_pos())

    def mouse_press_event(self, e):
        if sys.platform == "win32" or not self.can_drag(e.pos()):
            return

        startSystemMove(self.window(), e.global_pos())

    def __toggle_max_state(self):
        """Toggles the maximization state of the window and change icon"""
        if self.window().is_maximized():
            self.window().show_normal()
        else:
            self.window().show_maximized()

    def _is_drag_region(self, pos):
        """Check whether the position belongs to the area where dragging is allowed"""
        width = 0
        for button in self.find_children(TitleBarButton):
            if button.is_visible():
                width += button.width()

        return 0 < pos.x() < self.width() - width

    def _has_button_pressed(self):
        """whether any button is pressed"""
        return any(btn.is_pressed() for btn in self.find_children(TitleBarButton))

    def can_drag(self, pos):
        """whether the position is draggable"""
        return self._is_drag_region(pos) and not self._has_button_pressed()

    def set_double_click_enabled(self, is_enabled):
        """whether to switch window maximization status when double clicked
        Parameters
        ----------
        isEnabled: bool
            whether to enable double click
        """
        self._is_double_click_enabled = is_enabled


class TitleBar(TitleBarBase):
    """Title bar"""

    def __init__(self, parent):
        super().__init__(parent)
        self.hbox_layout = QHBoxLayout(self)

        # add buttons to layout
        self.hbox_layout.set_spacing(0)
        self.hbox_layout.set_contents_margins(0, 0, 0, 0)
        self.hbox_layout.set_alignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hbox_layout.add_stretch(1)
        self.hbox_layout.add_widget(self.min_btn, 0, Qt.AlignRight)
        self.hbox_layout.add_widget(self.max_btn, 0, Qt.AlignRight)
        self.hbox_layout.add_widget(self.close_btn, 0, Qt.AlignRight)


class StandardTitleBar(TitleBar):
    """Title bar with icon and title"""

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.icon_label = QLabel(self)
        self.icon_label.set_fixed_size(20, 20)
        self.hbox_layout.insert_spacing(0, 10)
        self.hbox_layout.insert_widget(1, self.icon_label, 0, Qt.AlignLeft)
        self.window().windowIconChanged.connect(self.set_icon)

        # add title label
        self.title_label = QLabel(self)
        self.hbox_layout.insert_widget(2, self.title_label, 0, Qt.AlignLeft)
        self.title_label.set_style_sheet(
            """
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px
            }
            """
        )
        self.window().windowTitleChanged.connect(self.set_title)

    def set_title(self, title):
        """set the title of title bar
        Parameters
        ----------
        title: str
            the title of title bar
        """
        self.title_label.set_text(title)
        self.title_label.adjust_size()

    def set_icon(self, icon):
        """set the icon of title bar
        Parameters
        ----------
        icon: QIcon | QPixmap | str
            the icon of title bar
        """
        self.icon_label.set_pixmap(QIcon(icon).pixmap(20, 20))
