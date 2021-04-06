from tkinter import *
import tkinter.filedialog, tkinter.messagebox
import pyautogui as pg
import datetime


def PyPad():
    root = Tk()
    root.title("Untitled - PyPad")
    root.geometry("500x500")

    scrollbar_y = Scrollbar(root)
    scrollbar_y.pack(side = RIGHT, fill = Y)

    scrollbar_x = Scrollbar(root, orient='horizontal')
    scrollbar_x.pack(side = BOTTOM, fill = X)

    textfield = Text(root, wrap = "none", tabs=4, yscrollcommand = scrollbar_y.set, xscrollcommand = scrollbar_x.set, undo=True, autoseparators=True, maxundo=-1)
    textfield.pack(expand = True, fill=BOTH)

    scrollbar_y.config(command = textfield.yview )
    scrollbar_x.config(command = textfield.xview )

    k = TextWidget(root, textfield)

    ########## Toolbar ##########

    main_menu=Menu(root,bg="#cedbff",tearoff=0)

    file_menu=Menu(main_menu,tearoff=0)
    file_menu.add_command(label='New', command=k.new)
    file_menu.add_command(label='Open', command=k.open_file)
    file_menu.add_command(label='Save', command=k.save_file)
    file_menu.add_command(label='Save As', command=k.save_file_as)
    file_menu.add_command(label='Exit All', command=k.exit)

    edit_menu=Menu(main_menu,tearoff=0)
    edit_menu.add_command(label='Cut', command=k.cut)
    edit_menu.add_command(label='Copy', command=k.copy)
    edit_menu.add_command(label='Paste', command=k.paste)
    edit_menu.add_command(label='Delete', command=k.delete)
    edit_menu.add_command(label='Undo', command=k.undo)
    edit_menu.add_command(label='Select All', command=k.select_all)
    edit_menu.add_command(label='Time/Date', command=k.timedate)

    format_menu=Menu(main_menu,tearoff=0)
    format_menu.add_command(label='Font Color')
    format_menu.add_command(label='Font Style')
    format_menu.add_command(label='Font Size')
    format_menu.add_command(label='Word Wrap')

    view_menu=Menu(main_menu,tearoff=0)
    view_menu.add_command(label='Zoom In')
    view_menu.add_command(label='Zoom Out')
    view_menu.add_command(label='Status Bar')

    main_menu.add_cascade(label='File', menu = file_menu)
    main_menu.add_cascade(label='Edit', menu = edit_menu)
    main_menu.add_cascade(label='Format', menu = format_menu)
    main_menu.add_cascade(label='View', menu = view_menu)
    main_menu.add_command(label='About', command=k.about)

    root.config(menu=main_menu)

    root.mainloop()



class TextWidget:
    def __init__(self, root, text):
        self.root = root
        self.text = text 
        self.filename = ''
        self._filetypes = [
        ('Text', '*.txt'),
            ('All files', '*'),
        ]
    
    def save_file(self):
        if (self.filename == ''):
            self.save_file_as()
        else:
            f = open(self.filename, 'w')
            f.write(self.text.get('1.0', 'end-1c'))
            f.close()
            tkinter.messagebox.showinfo('PyPad', 'File Saved')

    def save_file_as(self):
        temp = tkinter.filedialog.asksaveasfilename(defaultextension='.txt', filetypes = self._filetypes)
        if temp:
            self.filename = temp
            f = open(self.filename, 'w')
            f.write(self.text.get('1.0', 'end-1c'))
            f.close()
            self.root.title(f"{self.filename} - PyPad") 
            tkinter.messagebox.showinfo('PyPad', 'File Saved')

    def open_file(self, filename = None):
        if not filename:
            self.filename = tkinter.filedialog.askopenfilename(filetypes = self._filetypes)
        else:
            self.filename = filename
            
        if not (self.filename == ''):
            f = open(self.filename, 'r')
            f2 = f.read()
            self.text.delete('1.0', 'end')
            self.text.insert('1.0', f2)
            f.close()
            self.root.title(f"{self.filename} - PyPad") 

    def new(self):
        PyPad()

    def exit(self):
        exit()

    def cut(self):
        pg.hotkey('ctrl','x')
    
    def copy(self):
        pg.hotkey('ctrl','c')

    def paste(self):
        pg.hotkey('ctrl','v')

    def undo(self):
        pg.hotkey('ctrl','z')

    def select_all(self):
        pg.hotkey('ctrl','a')

    def delete(self):
        pg.press('delete')

    def timedate(self):
        tad = datetime.datetime.now()
        self.text.insert("insert", tad)

    def about(self):
        tkinter.messagebox.showinfo('PyPad', 'A simple Notepad clone written in python\n\n~ Made by Ronik Bhattacharjee')




if __name__ == "__main__":
    PyPad()