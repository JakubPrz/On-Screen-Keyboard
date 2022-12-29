from typing import Union
from tkinter import Tk, Toplevel


def center_window(win: Union[Tk, Toplevel], move_x: int = 0, move_y: int = 0):
    """
    Centers the window on the screen.

    Args:
        win: The window to center.
        move_x: Offset in the x-axis from the center.
        move_y: Offset in the y-axis from the center.
    """

    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2 + move_x
    y = win.winfo_screenheight() // 2 - win_height // 2 + move_y
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
