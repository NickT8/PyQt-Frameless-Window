# coding:utf-8
import Cocoa
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from ..utils.mac_utils import get_ns_window


class QMacCocoaViewContainer(QWidget):
    def __init__(self, view, parent=None):
        super().__init__(parent=parent)
        self.set_attribute(Qt.WA_NativeWindow)


class MacWindowEffect:
    """Mac OS window effect"""

    def __init__(self, window):
        self.window = window

    def set_acrylic_effect(
        self, hWnd, gradientColor="F2F2F230", isEnableShadow=True, animationId=0
    ):
        """set acrylic effect for window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            window handle

        gradientColor: str
            hexadecimal acrylic mixed color, corresponding to RGBA components

        isEnableShadow: bool
            whether to enable window shadow

        animationId: int
            turn on blur animation or not
        """
        frame = Cocoa.NSMakeRect(0, 0, self.window.width(), self.window.height())
        visualEffectView = Cocoa.NSVisualEffectView.new()
        visualEffectView.setAutoresizingMask_(
            Cocoa.NSViewWidthSizable | Cocoa.NSViewHeightSizable
        )  # window resizable
        visualEffectView.setFrame_(frame)
        visualEffectView.setState_(Cocoa.NSVisualEffectStateActive)

        # https://developer.apple.com/documentation/appkit/nsvisualeffectmaterial
        visualEffectView.setMaterial_(Cocoa.NSVisualEffectMaterialPopover)
        visualEffectView.setBlendingMode_(Cocoa.NSVisualEffectBlendingModeBehindWindow)

        nsWindow = get_ns_window(self.window.win_id())
        content = nsWindow.contentView()
        container = QMacCocoaViewContainer(0, self.window)
        content.addSubview_positioned_relativeTo_(visualEffectView, Cocoa.NSWindowBelow, container)

    def set_mica_effect(self, hWnd, isDarkMode=False, isAlt=False):
        """Add mica effect to the window (Win11 only)

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        isDarkMode: bool
            whether to use dark mode mica effect

        isAlt: bool
            whether to use mica alt effect
        """
        self.set_acrylic_effect(hWnd)

    def set_aero_effect(self, hWnd):
        """add Aero effect to the window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        self.set_acrylic_effect(hWnd)

    def set_transparent_effect(self, hWnd):
        """set transparent effect for window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        pass

    def remove_background_effect(self, hWnd):
        """Remove background effect

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        pass

    def add_shadow_effect(self, hWnd):
        """add shadow to window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        get_ns_window(hWnd).setHasShadow_(True)

    def add_menu_shadow_effect(self, hWnd):
        """add shadow to menu

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        self.add_shadow_effect(hWnd)

    @staticmethod
    def remove_menu_shadow_effect(hWnd):
        """Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        get_ns_window(hWnd).setHasShadow_(False)

    def remove_shadow_effect(self, hWnd):
        """Remove shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        get_ns_window(hWnd).setHasShadow_(False)

    @staticmethod
    def add_window_animation(hWnd):
        """Enables the maximize and minimize animation of the window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        pass

    @staticmethod
    def disable_maximize_button(hWnd):
        """Disable the maximize button of window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """

    def enable_blur_behind_window(self, hWnd):
        """enable the blur effect behind the whole client
        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass
