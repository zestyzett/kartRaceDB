from tkinter import *
root = Tk()

e = Entry(root, width=50)
e.pack()
e.insert(0, "enter your name")

def my_click():
    hello = 'Hello ' + e.get()
    myLabel = Label(root, text=hello)
    myLabel.pack()


my_button = Button(root, text='click me', command = my_click, bg = '#fafafa', borderwidth = 0)

my_button.pack()


root.mainloop()

