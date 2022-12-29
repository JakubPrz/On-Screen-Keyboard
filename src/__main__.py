from tkinter import Tk, PhotoImage, Button, Entry
from tkinter.font import Font

from src.keyboard.window_configuration import center_window
from src.keyboard.on_screen_keyboard import OnScreenKeyboard


def main():
    master = Tk()
    width = 1024
    height = 530
    master.geometry(f"{str(width)}x{str(height)}")
    center_window(win=master)
    entry = Entry(master,
                  width=33,
                  font=Font(family="Helvetica", size=12),
                  bg="white",
                  borderwidth=0,
                  highlightthickness=0)

    keyboard_icon = PhotoImage(file="images/keyboard_icon.png")
    button = Button(image=keyboard_icon, borderwidth=0)
    entry.pack(pady=50)
    button.pack()

    hide_img = PhotoImage(file="images/hide_icon.png")
    keyboard = OnScreenKeyboard(master=master, width=1024, height=280, output_entry=entry, hide_img=hide_img)

    button.config(command=lambda: keyboard.display())
    master.mainloop()


if __name__ == '__main__':
    main()
