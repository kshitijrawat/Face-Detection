import atte as back
from tkinter import *
from tkinter import messagebox


root = Tk()
root.title("Attendance System")
root.geometry('800x465')
img = PhotoImage(file="save.png")
label = Label(root,image=img).place(x=0, y=0, relwidth=1, relheight=1)
frame = Frame(root)
frame.pack(pady=90)
btn = Button(frame, text='Start recording',padx=20,pady=10,activeforeground = "white",activebackground="black",command=lambda :back.new(),)
btn.pack()
messagebox.showinfo("showinfo", "please wait a little for photos are being encoded")
root.mainloop()
