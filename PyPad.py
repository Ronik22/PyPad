"""
    A Text Editor written in Python with some additional features other than the basic features of Notepad.
    ~ Ronik Bhattacharjee
"""


from tkinter import *
import tkinter.filedialog, tkinter.messagebox, tkinter.colorchooser, tkinter.font, tkinter.ttk
import pyautogui as pg
import datetime
from tkfontchooser import askfont
import webbrowser
from googletrans import Translator
from tkinter.scrolledtext import ScrolledText
import pyttsx3
import speech_recognition as sr
from threading import Thread
import re


def PyPad():
    root = Tk()
    root.title("Untitled - PyPad")
    root.geometry("600x600")

    # Setting icon of master window
    icon = PhotoImage(file = 'ppad.png')
    root.iconphoto(False, icon)

    status_bar = Frame(master=root,bg="#ededed",height=30, highlightthickness=1, highlightbackground="#cecece")    
    status_bar.pack(side=BOTTOM,fill=X)

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
    file_menu.add_separator()
    file_menu.add_command(label='Exit All', command=k.exit)

    edit_menu=Menu(main_menu,tearoff=0)
    edit_menu.add_command(label='Cut', command=k.cut)
    edit_menu.add_command(label='Copy', command=k.copy)
    edit_menu.add_command(label='Paste', command=k.paste)
    edit_menu.add_command(label='Delete', command=k.delete)
    edit_menu.add_separator()
    edit_menu.add_command(label='Undo', command=textfield.edit_undo)
    edit_menu.add_command(label='Redo', command=textfield.edit_redo)
    edit_menu.add_command(label='Select All', command=k.select_all)
    edit_menu.add_separator()
    edit_menu.add_command(label='Time/Date', command=k.timedate)

    format_menu=Menu(main_menu,tearoff=0)
    format_menu.add_command(label='Font Color', command=k.font_color)
    format_menu.add_command(label='Font Style', command=k.font_style)
    format_menu.add_separator()
    format_menu.add_command(label='Word Wrap', command=k.word_wrap)

    view_menu=Menu(main_menu,tearoff=0)
    view_menu.add_command(label='Evaluate', command=k.evaluate)
    view_menu.add_command(label='Translate', command=k.translate)
    view_menu.add_separator()
    view_menu.add_command(label='Text to Speech', command=k.text_to_speech)
    view_menu.add_command(label='Speech to Text', command=k.speech_to_text)
    view_menu.add_separator()
    view_menu.add_command(label='Search on web', command=k.search_on_web)
    view_menu.add_command(label='Goto URL', command=k.goto_url)
    view_menu.add_separator()
    view_menu.add_command(label='To UpperCase', command=k.to_upper_case)
    view_menu.add_command(label='To LowerCase', command=k.to_lower_case)
    view_menu.add_separator()
    view_menu.add_command(label='Total Characters', command=k.char_len)
    view_menu.add_command(label='Total Words', command=k.how_many_words)

    main_menu.add_cascade(label='File', menu = file_menu)
    main_menu.add_cascade(label='Edit', menu = edit_menu)
    main_menu.add_cascade(label='Format', menu = format_menu)
    main_menu.add_cascade(label='Options', menu = view_menu)
    main_menu.add_command(label='About', command=k.about)

    root.config(menu=main_menu)

    # STATUS BAR

    def i_r_c(text):
        mtext = text.split(".")
        t = "Line "+mtext[0]+", Col "+mtext[1]
        return t

    idx = Label(status_bar, text=i_r_c(textfield.index(tkinter.INSERT)))  
    idx.pack(side=RIGHT)

    def update_statusbar(*args):
        m = i_r_c(textfield.index(tkinter.INSERT))
        idx["text"] = m

    root.bind("<Key>", update_statusbar)

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
        
        # SPELL CHECK
        self.text.tag_configure("misspelled", foreground="red", underline=True)
        self._words=open("./words_alpha.txt").read().split("\n")   # Wordlist Link : https://github.com/dwyl/english-words

        # LINK CHECK
        self.text.tag_configure("url", foreground="blue", underline=True)

        text.bind("<space>", lambda x: [self.Spellcheck(x), self.tag_links(x)])
        

    def Spellcheck(self, event):
        index = self.text.search(r'\s', "insert", backwards=True, regexp=True)
        if index == "":
            index ="1.0"
        else:
            index = self.text.index("%s+1c" % index)
        word = self.text.get(index, "insert")
        if word in self._words:
            self.text.tag_remove("misspelled", index, "%s+%dc" % (index, len(word)))
        else:
            self.text.tag_add("misspelled", index, "%s+%dc" % (index, len(word)))


    def tag_links(self, event):

        index = self.text.search(r'\s', "insert", backwards=True, regexp=True)
        if index == "":
            index ="1.0"
        else:
            index = self.text.index("%s+1c" % index)
        word = self.text.get(index, "insert")

        regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
        p = re.compile(regex)
    
        if(re.search(p, word)):
            self.text.tag_add("url", index, "%s+%dc" % (index, len(word)))
        else:
            self.text.tag_remove("url", index, "%s+%dc" % (index, len(word)))


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

        sel = None

        def translation_opt():
            t = opt_var.get()
            translator = Translator(service_urls=['translate.googleapis.com'])
            translation=translator.translate(var2.get(),dest=t)
            textbox.replace("1.0", END, translation.text)
            # var2.set(translation.text)

        lang_list = [
            'afrikaans',
            'albanian',
            'amharic',
            'arabic',
            'armenian',
            'azerbaijani',
            'basque',
            'belarusian',
            'bengali',
            'bosnian',
            'bulgarian',
            'catalan',
            'cebuano',
            'chichewa',
            'chinese (simplified)',
            'chinese (traditional)',
            'corsican',
            'croatian',
            'czech',
            'danish',
            'dutch',
            'english',
            'esperanto',
            'estonian',
            'filipino',
            'finnish',
            'french',
            'frisian',
            'galician',
            'georgian',
            'german',
            'greek',
            'gujarati',
            'haitian creole',
            'hausa',
            'hawaiian',
            'hebrew',
            'hebrew',
            'hindi',
            'hmong',
            'hungarian',
            'icelandic',
            'igbo',
            'indonesian',
            'irish',
            'italian',
            'japanese',
            'javanese',
            'kannada',
            'kazakh',
            'khmer',
            'korean',
            'kurdish (kurmanji)',
            'kyrgyz',
            'lao',
            'latin',
            'latvian',
            'lithuanian',
            'luxembourgish',
            'macedonian',
            'malagasy',
            'malay',
            'malayalam',
            'maltese',
            'maori',
            'marathi',
            'mongolian',
            'myanmar (burmese)',
            'nepali',
            'norwegian',
            'odia',
            'pashto',
            'persian',
            'polish',
            'portuguese',
            'punjabi',
            'romanian',
            'russian',
            'samoan',
            'scots gaelic',
            'serbian',
            'sesotho',
            'shona',
            'sindhi',
            'sinhala',
            'slovak',
            'slovenian',
            'somali',
            'spanish',
            'sundanese',
            'swahili',
            'swedish',
            'tajik',
            'tamil',
            'telugu',
            'thai',
            'turkish',
            'ukrainian',
            'urdu',
            'uyghur',
            'uzbek',
            'vietnamese',
            'welsh',
            'xhosa',
            'yiddish',
            'yoruba',
            'zulu',
        ]
        try:
            sel = self.text.selection_get()
        except:
            tkinter.messagebox.showinfo('PyPad', 'You need to select something to translate')
        
        if sel:
            try:
                master = Toplevel(self.root)
                master.geometry("600x600")
                master.title("Translation - PyPad")
                master["bg"] = "#fff"
                tools_area = Frame(master=master,bg="#1F7DFF",width=100)      
                tools_area.pack(side=LEFT,fill=Y)

                var2 = StringVar()  # to be translated
                var2.set(sel)

                opt_var = StringVar(master)
                opt_var.set('Hindi')   # default option

                opt_frame = LabelFrame(master=tools_area,bg="#1F7DFF",fg="#fff",text="Select Language",labelanchor='n',relief=GROOVE,bd=1)   
                opt_frame.pack(anchor="center",padx=10,pady=20)
                e = tkinter.ttk.Combobox(opt_frame, textvariable=opt_var, values=lang_list)
                e.pack(anchor="center",padx=10,pady=10)

                textbox = ScrolledText(master, bg="#fff", wrap = tkinter.WORD)
                textbox.pack(expand = True, fill=BOTH)
                textbox.insert("insert", var2.get())
                # textbox = Label(master, textvariable=var2, bg="#fff").pack(expand = True, fill=BOTH)

                Button(tools_area, width=8, height=1,relief=FLAT, text='Translate',command=translation_opt).pack(padx=12,pady=10,anchor="center", side=BOTTOM)
                master.mainloop()
                
            except Exception as e:
                tkinter.messagebox.showinfo('PyPad', e)
    
    def text_to_speech(self):
        try:
            sel = self.text.selection_get()
            engine = pyttsx3.init()
            engine.say(sel)
            engine.runAndWait()
        except Exception as e:
            tkinter.messagebox.showinfo('PyPad', "Select something to convert to speech")


    def speech_to_text(self):
        def capture():
            rec = sr.Recognizer()
            with sr.Microphone() as source:
                audio = rec.listen(source, phrase_time_limit=5)
            try:
                text = rec.recognize_google(audio, language='en-US')
                return text
            except:
                return 0
        
        while 1:
            captured_text = capture().lower()
            if captured_text == 0:
                continue
            if 'quit' in str(captured_text):
                break
            self.text.insert("insert", captured_text)
    

    def search_on_web(self):
        try:
            sel = self.text.selection_get()
            webbrowser.open(f'https://www.google.com/search?q={sel}')
        except:
            tkinter.messagebox.showinfo('PyPad', 'You need to select something to search on web')

    def goto_url(self):
        try:
            sel = self.text.selection_get()
            webbrowser.open_new(sel)
        except:
            tkinter.messagebox.showinfo('PyPad', 'Select a link. Valid links will be underlined and highlighted in blue.')


    def to_upper_case(self):
        try:
            sel = self.text.selection_get()
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.text.insert("insert", sel.upper())
        except Exception as e:
            tkinter.messagebox.showinfo('PyPad', "Select something")

    def to_lower_case(self):
        try:
            sel = self.text.selection_get()
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.text.insert("insert", sel.lower())
        except Exception as e:
            tkinter.messagebox.showinfo('PyPad', "Select something")

    def char_len(self):
        try:
            sel = self.text.selection_get()
            tkinter.messagebox.showinfo('PyPad', "Total Characters: " + str(len(sel)))
        except Exception as e:
            tkinter.messagebox.showinfo('PyPad', "Select something")

    def how_many_words(self):
        try:
            sel = self.text.selection_get()
            tkinter.messagebox.showinfo('PyPad', "Word Count: " + str(len(sel.split())))
        except Exception as e:
            tkinter.messagebox.showinfo('PyPad', "Select something")


    def word_wrap(self):
        if self.text["wrap"] == "none":
            self.text["wrap"] = "word"
        else:
            self.text["wrap"] = "none"

    def about(self):
        tkinter.messagebox.showinfo('PyPad', ' A Text Editor written in Python with some additional features other than the basic features of Notepad.\n\n~ Made by Ronik Bhattacharjee')




if __name__ == "__main__":
    PyPad()