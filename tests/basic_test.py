from tkinter import *


def hello():
    print("Hello from master Interactor")


def open_user_interface():
    window = Tk()
    window.geometry("500x500")
    start_button = Button(window, text='Start', command=hello)
    start_button.place(x=250, y=250)
    window.mainloop()
