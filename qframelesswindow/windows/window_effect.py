# coding:utf-8
import sys
import warnings
from ctypes import POINTER, WinDLL, byref, c_bool, c_int, pointer, sizeof
from ctypes.wintypes import DWORD, LONG, LPCVOID

import win32api
import win32con
import win32gui

from ..utils.win32_utils import (
    is_composition_enabled,
    is_greater_equal_win10,
    is_greater_equal_win11,
)
from .c_structures import (
    ACCENT_POLICY,
    ACCENT_STATE,
    DWM_BLURBEHIND,
    DWMNCRENDERINGPOLICY,
    DWMWINDOWATTRIBUTE,
    MARGINS,
    WINDOWCOMPOSITIONATTRIB,
    WINDOWCOMPOSITIONATTRIBDATA,
)


class WindowsWindowEffect:
    """Windows window effect"""

    def __init__(self, window):
        self.window = window

        # Declare the function signature of the API
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmEnableBlurBehindWindow = self.dwmapi.DwmEnableBlurBehindWindow
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute

        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmEnableBlurBehindWindow.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG

        self.SetWindowCompositionAttribute.argtypes = [
            c_int,
            POINTER(WINDOWCOMPOSITIONATTRIBDATA),
        ]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]
        self.DwmEnableBlurBehindWindow.argtypes = [c_int, POINTER(DWM_BLURBEHIND)]

        # Initialize structure
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.winCompAttrData.SizeOfData = sizeof(self.accentPolicy)
        self.winCompAttrData.Data = pointer(self.accentPolicy)

    def set_acrylic_effect(self, hWnd, gradientColor="F2F2F299", enableShadow=True, animationId=0):
        """Add the acrylic effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        gradientColor: str
            Hexadecimal acrylic mixed color, corresponding to four RGBA channels

        isEnableShadow: bool
            Enable window shadows

        animationId: int
            Turn on matte animation
        """
        if not is_greater_equal_win10():
            warnings.warn("The acrylic effect is only available on Win10+")
            return

        hWnd = int(hWnd)
        gradientColor = "".join(gradientColor[i : i + 2] for i in range(6, -1, -2))
        gradientColor = DWORD(int(gradientColor, base=16))
        animationId = DWORD(animationId)
        accentFlags = DWORD(0x20 | 0x40 | 0x80 | 0x100) if enableShadow else DWORD(0)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def set_mica_effect(self, hWnd, isDarkMode=False, isAlt=False):
        """Add the mica effect to the window (Win11 only)

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle

        isDarkMode: bool
            whether to use dark mode mica effect

        isAlt: bool
            whether to enable mica alt effect
        """
        if not is_greater_equal_win11():
            warnings.warn("The mica effect is only available on Win11")
            return

        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_HOSTBACKDROP.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

        if isDarkMode:
            self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_USEDARKMODECOLORS.value
            self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

        if sys.getwindowsversion().build < 22523:
            self.DwmSetWindowAttribute(hWnd, 1029, byref(c_int(1)), 4)
        else:
            self.DwmSetWindowAttribute(hWnd, 38, byref(c_int(4 if isAlt else 2)), 4)

        self.DwmSetWindowAttribute(hWnd, 20, byref(c_int(1 * isDarkMode)), 4)

    def set_aero_effect(self, hWnd):
        """Add the aero effect to the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.winCompAttrData.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    def remove_background_effect(self, hWnd):
        """Remove background effect

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.accentPolicy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value
        self.SetWindowCompositionAttribute(hWnd, pointer(self.winCompAttrData))

    @staticmethod
    def move_window(hWnd):
        """Move the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        win32gui.ReleaseCapture()
        win32api.SendMessage(hWnd, win32con.WM_SYSCOMMAND, win32con.SC_MOVE + win32con.HTCAPTION, 0)

    def add_shadow_effect(self, hWnd):
        """Add DWM shadow to window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        if not is_composition_enabled():
            return

        hWnd = int(hWnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    def add_menu_shadow_effect(self, hWnd):
        """Add DWM shadow to menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        if not is_composition_enabled():
            return

        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_ENABLED.value)),
            4,
        )
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(hWnd, byref(margins))

    def remove_shadow_effect(self, hWnd):
        """Remove DWM shadow from the window

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        self.DwmSetWindowAttribute(
            hWnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_DISABLED.value)),
            4,
        )

    @staticmethod
    def remove_menu_shadow_effect(hWnd):
        """Remove shadow from pop-up menu

        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        style = win32gui.GetClassLong(hWnd, win32con.GCL_STYLE)
        style &= ~0x00020000  # CS_DROPSHADOW
        win32api.SetClassLong(hWnd, win32con.GCL_STYLE, style)

    @staticmethod
    def add_window_animation(hWnd):
        """Enables the maximize and minimize animation of the window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MINIMIZEBOX
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )

    @staticmethod
    def disable_maximize_button(hWnd):
        """Disable the maximize button of window

        Parameters
        ----------
        hWnd : int or `sip.voidptr`
            Window handle
        """
        hWnd = int(hWnd)
        style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            hWnd,
            win32con.GWL_STYLE,
            style & ~win32con.WS_MAXIMIZEBOX,
        )

    def enable_blur_behind_window(self, hWnd):
        """enable the blur effect behind the whole client
        Parameters
        ----------
        hWnd: int or `sip.voidptr`
            Window handle
        """
        blurBehind = DWM_BLURBEHIND(1, True, 0, False)
        self.DwmEnableBlurBehindWindow(int(hWnd), byref(blurBehind))
