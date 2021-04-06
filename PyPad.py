from tkinter import *
import tkinter.filedialog, tkinter.messagebox, tkinter.colorchooser, tkinter.font
import pyautogui as pg
import datetime
from tkfontchooser import askfont
import webbrowser
from googletrans import Translator


var1 = ""

def translation_opt(sel, lan):
    global var1
    translator = Translator(service_urls=['translate.googleapis.com'])
    translation=translator.translate(sel,dest=lan)
    var1.set(translation.text)


def PyPad():
    root = Tk()
    root.title("Untitled - PyPad")
    root.geometry("500x500")

    scrollbar_y = Scrollbar(root)
    scrollbar_y.pack(side = RIGHT, fill = Y)

    scrollbar_x = Scrollbar(root, orient='horizontal')
    scrollbar_x.pack(side = BOTTOM, fill = X)

    textfield = Text(root, 
                    wrap = "none", 
                    tabs=4, 
                    yscrollcommand = scrollbar_y.set, 
                    xscrollcommand = scrollbar_x.set, 
                    undo=True, autoseparators=True, 
                    maxundo=-1,
                    font=("Arial", 12))

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
    edit_menu.add_command(label='Redo', command=k.redo)
    edit_menu.add_command(label='Select All', command=k.select_all)
    edit_menu.add_command(label='Time/Date', command=k.timedate)

    format_menu=Menu(main_menu,tearoff=0)
    format_menu.add_command(label='Font Color', command=k.font_color)
    format_menu.add_command(label='Font Style', command=k.font_style)
    format_menu.add_command(label='Word Wrap', command=k.word_wrap)

    view_menu=Menu(main_menu,tearoff=0)
    view_menu.add_command(label='Evaluate', command=k.evaluate)
    view_menu.add_command(label='Translate', command=k.translate)
    view_menu.add_command(label='Pronounce', command=k.pronounce)
    view_menu.add_command(label='Search on web', command=k.search_on_web)
    view_menu.add_command(label='Status Bar')

    main_menu.add_cascade(label='File', menu = file_menu)
    main_menu.add_cascade(label='Edit', menu = edit_menu)
    main_menu.add_cascade(label='Format', menu = format_menu)
    main_menu.add_cascade(label='Options', menu = view_menu)
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

    def redo(self):
        pg.hotkey('ctrl','shift', 'z')

    def select_all(self):
        pg.hotkey('ctrl','a')

    def delete(self):
        pg.press('delete')

    def timedate(self):
        tad = datetime.datetime.now()
        self.text.insert("insert", tad)

    def font_color(self):
        new_color = tkinter.colorchooser.askcolor()[1]
        self.text['fg'] = new_color

    def font_style(self):
        font = askfont(self.root)
        if font:
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'

            self.text["font"] = font_str

    def evaluate(self):
        try:
            sel = self.text.selection_get()
            try:
                value = eval(sel)
                tkinter.messagebox.showinfo('PyPad', f'The answer is : {value}')
            except Exception as e:
                tkinter.messagebox.showinfo('PyPad', "Invalid expression")
        except:
            tkinter.messagebox.showinfo('PyPad', 'You need to select something to evaluate')


    def translate(self):
        try:
            sel = self.text.selection_get()
            top = Toplevel(self.root) 
            top.title("Translation - PyPad") 
            top.geometry("300x300")

            lan = StringVar(top)
            lan.set('Hindi')
            choices = { 'English','Hindi','Gujarati','Spanish','German'}
            lan_menu = OptionMenu( top, lan, *choices)
            Label(top,text="Select a language").pack()
            lan_menu.pack()

            var1 = StringVar(top)
            Button(top,text='Translate',command=translation_opt(sel, lan)).pack()
            output = Label(top, text=var1)
            output.pack()
            top.mainloop() 
        except Exception as e:
            tkinter.messagebox.showinfo('PyPad', e)
    
    def pronounce(self):
        pass
    
    def search_on_web(self):
        try:
            sel = self.text.selection_get()
            webbrowser.open(f'https://www.google.com/search?q={sel}')
        except:
            tkinter.messagebox.showinfo('PyPad', 'You need to select something to search on web')


    def word_wrap(self):
        if self.text["wrap"] == "none":
            self.text["wrap"] = "word"
        else:
            self.text["wrap"] = "none"

    def about(self):
        tkinter.messagebox.showinfo('PyPad', 'A writing pad written in python.\n\n~ Made by Ronik Bhattacharjee')




if __name__ == "__main__":
    PyPad()