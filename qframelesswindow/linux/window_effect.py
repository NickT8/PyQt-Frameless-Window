# coding:utf-8


class LinuxWindowEffect:
    """Linux window effect"""

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
        pass

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
        pass

    def set_aero_effect(self, hWnd):
        """add Aero effect to the window

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

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
        pass

    def add_menu_shadow_effect(self, hWnd):
        """add shadow to menu

        Parameter
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    @staticmethod
    def remove_menu_shadow_effect(hWnd):
        """Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

    def remove_shadow_effect(self, hWnd):
        """Remove shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        pass

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
