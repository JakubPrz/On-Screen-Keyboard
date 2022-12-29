from tkinter import Tk, Toplevel, Frame, PhotoImage, Entry, Button, END, INSERT
from tkinter.font import Font
from typing import Any

from src.keyboard.utils import do_for_letter_keys, remove_char, insert_char
from src.keyboard.window_configuration import center_window
from src.keyboard.keys import keys, polish_chars
from src.keyboard.button_sizes import sizes
from src.keyboard.color_themes import *


class OnScreenKeyboard(Toplevel):
    """
    Implementation of on-screen keyboard for the LPM application.
    This keyboard is without unnecessary buttons,
    supports entering Polish characters and
    passes output directly to the given tkinter.Entry.
    This virtual keyboard is sized for use on a 7' display.

    Attributes:
        master: The main window of app.
        width: Width of the keyboard window.
        height: Height of the keyboard window.
        output_entry: Entry object for passes an output.
        hide_img: PhotoImage instance with loaded image file.

    Usage:
        # Assign instance of the PhotoImage class
        # with loaded image file to a variable.
        hide_img = tkinter.PhotoImage(file="hide.png")

        # Create on-screen keyboard, pass img
        keyboard = OnScreenKeyboard(master=master, width=1024, height=280,
                                    output_entry=entry, hide_img=hide_img)

        # Display it
        keyboard.display()

        # To hide it, use hide() method.
    """

    def __init__(self, master: Tk, width: int, height: int, output_entry: Entry, hide_img: PhotoImage):
        """
        Constructs all the necessary attributes for the OnScreenKeyboard object.
        Initialization of on-screen keyboard.

        Args:
            master: The main window of app.
            width: Width of the keyboard window.
            height: Height of the keyboard window.
            output_entry: Entry object for passes an output.
            hide_img: PhotoImage instance with loaded image file.
        """

        Toplevel.__init__(self, master)

        # Configuring keyboard window
        self.geometry(f"{str(width)}x{str(height)}")
        self.overrideredirect(True)
        center_window(win=self, move_y=130)
        self.withdraw()  # hide it fast, it's only initialization
        self.configure(bg=WHITE_COL)
        self.attributes("-topmost", True)  # keyboard always on top
        self.resizable(False, False)

        # Key states
        self._alt = False
        self._shift = False
        self._caps = False

        self.buttons = []
        self._output_entry = output_entry

        # Creating button for hiding keyboard
        hide_button = Button(self, image=hide_img, borderwidth=0,
                             bg=WHITE_COL, activebackground=WHITE_COL, command=self.withdraw)
        hide_button.pack(anchor="ne", padx=7)

        # Creating keyboard keys and placing them
        btn_height = 0

        y = 15
        for row in keys:
            x = 35
            for key in row:
                btn_width = 0.08035 * width
                btn_height = 0.23 * height

                padx = round(btn_width/10)
                pady = round(btn_height/10)

                frame = Frame(self, highlightbackground=WHITE_COL, highlightthickness=4)

                btn = Button(frame, activebackground=ACCENT_COL, text=key,
                             bg=LIGHT_GREY_COL, fg=WHITE_COL, relief="flat", padx=padx, pady=pady,
                             borderwidth=0, anchor="nw", font=Font(size=13))

                try:
                    btn_width *= sizes[key]
                except KeyError:
                    # use default size button
                    pass

                btn.place(x=0, y=0, width=btn_width, height=btn_height)
                frame.place(x=x, y=y, width=btn_width, height=btn_height)

                x += btn_width

                # Bind events
                btn.bind("<ButtonPress-1>", lambda e: self._press(e))
                btn.bind("<Enter>", lambda e: self._enter(e))
                btn.bind("<Leave>", lambda e: self._leave(e))

                self.buttons.append(btn)

            y += btn_height

    def display(self):
        """ Displays on-screen keyboard. """

        self.deiconify()

    def hide(self):
        """ Hides on-screen keyboard. """

        self.withdraw()

    # ----------------------------- Handlers -----------------------------

    @staticmethod
    def _enter(event: Any):
        """
        Handling function when entering the button.
        It changes button background and text color when entering the button.

        Args:
            event: <Enter> event.
        """

        event.widget.configure(bg=DARK_GREY_COL, fg=BLACK_COL)

    @staticmethod
    def _leave(event: Any):
        """
        Handling function when leaving the button.
        It changes button background and text color when leaving the button.

        Args:
            event: <Leave> event.
        """

        event.widget.configure(bg=LIGHT_GREY_COL, fg=WHITE_COL)

    def _press(self, event: Any):
        """
        Handling function when pressing the button.
        It handles pressing all buttons.

        Args:
            event: <ButtonPress-1> event.
        """

        key = event.widget["text"]

        match key:
            case "Backspace":
                self._remove_char()

            case "Caps":
                if self._caps:  # Caps Lock is on
                    self._lower_keys()
                    self._caps = False
                else:  # Caps Lock is off
                    self._capitalize_keys()
                    self._caps = True

            case "Shift":
                if self._shift:
                    self._lower_keys()
                    self._shift = False
                else:
                    self._capitalize_keys()
                    self._shift = True

            case "Alt":
                if self._alt:
                    self.switch_off_polish_chars()
                    self._alt = False
                else:
                    self.switch_on_polish_chars()
                    self._alt = True

            case _:  # another keys
                self._insert_char(key)
                if self._shift:
                    self._lower_keys()
                    self._shift = False
                if self._alt:
                    self.switch_off_polish_chars()
                    self._alt = False

    # -------------------------- Other methods ---------------------------

    def _remove_char(self):
        """
        Removes character before the cursor's
        current position from entry field.
        """

        entry_text = self._output_entry.get()
        cursor_idx = self._output_entry.index(INSERT)
        # Remove character before cursor
        entry_text = remove_char(entry_text, index=cursor_idx - 1)
        self._output_entry.delete(0, END)
        self._output_entry.insert(END, entry_text)
        self._output_entry.icursor(cursor_idx - 1)

    def _insert_char(self, key: str):
        """
        Inserts character at the cursor's
        current position into entry field.
        """

        entry_text = self._output_entry.get()
        cursor_idx = self._output_entry.index(INSERT)
        # Insert character at cursor position
        entry_text = insert_char(entry_text, char=key, index=cursor_idx)
        self._output_entry.delete(0, END)
        self._output_entry.insert(END, entry_text)
        self._output_entry.icursor(cursor_idx + 1)

    @do_for_letter_keys
    def _capitalize_keys(self, button: Button):
        """
        Makes all letter keys upper case.

        Args:
            button: Button for keyboard key.
        """

        button.config(text=button['text'].capitalize())

    @do_for_letter_keys
    def _lower_keys(self, button: Button):
        """
        Reverts all letter keys to lower case.

        Args:
            button: Button for keyboard key.
        """

        button.config(text=button['text'].lower())

    @do_for_letter_keys
    def switch_on_polish_chars(self, button: Button):
        """
        Switching from ASCII to Polish letters on the keyboard.

        Args:
            button: Button of keyboard.
        """

        try:
            key = polish_chars[button['text']]
        except KeyError:
            pass
        else:
            button.config(text=key)

    @do_for_letter_keys
    def switch_off_polish_chars(self, button: Button):
        """
        Switching from Polish to ASCII letters on the keyboard.

        Args:
            button: Button of keyboard.
        """

        for k, v in polish_chars.items():
            if v == button['text']:
                button.config(text=k)
