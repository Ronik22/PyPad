# PyPad
A Text Editor written in Python with some additional features other than the basic features of Notepad.

## Additional Features
*   Speech to Text
*   Text to Speech
*   Search on Web
*   Translation
*   Auto Spell Check (Wordlist Link : https://github.com/dwyl/english-words)
*   Auto highlight and goto Links
*   Evaluation of simple mathematical expressions
*   Character and Word count
*   Custom Font Style and Color
*   Uppercase / Lowercase toggle

<br>

Links are `blue` and `underlined`.

Incorrect Spellings are `red` and `underlined`.

For Speech to Text say the word `quit` to stop transcription.

## Usage

### For direct use :

Go into the `build/PyPad` folder and double click on `PyPad.exe`

### For development purpose :

    $ git clone https://github.com/Ronik22/PyPad.git
    $ cd PyPad
    $ virtualenv venv
    $ . venv/bin/activate
    (venv) pip install -r requirements.txt
    (venv) python PyPad.py

Note for Python 3.4 users: replace `virtualenv` with `pyvenv`.

Note for Microsoft Windows users: replace the virtual environment activation command above with `venv\Scripts\activate`.
