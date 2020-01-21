from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from settings import *
from Building_AST import *


def run_command(funcname , filename):

    command = clang_command+funcname + " " + filename
    f = open(filepath, "w")
    f.write(command)
    f.close()
    create_subprocess_file_pipe(filepath, outfile)

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()

        self.title("Choose a file...")
        self.minsize(640, 400)

        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=0, row=1, padx=20, pady=20)

        self.button()



    def button(self):
        self.button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog).grid(column=1, row=1)


    def fileDialog(self):

        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=
        (("cpp files", "*.cpp"), ("all files", "*.*")))
        self.label = ttk.Label(self.labelFrame, text="")
        self.label.grid(column=1, row=2)
        self.label.configure(text=self.filename)
        names = search_func_names(self.filename)
        uniq_names = unique(names)
        print(uniq_names)
        self.lf = ttk.LabelFrame(self, text="FUNCTIONS")
        self.lf.grid(column=0, row=2, padx=20, pady=20)

        rownum = 1
        for func in uniq_names:
            self.func = ttk.Button(self.lf, text=func, command= lambda : run_command(func,self.filename)).grid(column=0,row=rownum)
            print(clang_command + func + " " + self.filename)
            rownum = rownum + 1



        self.myframe = ttk.Frame(self)
        self.window_frame = ttk.LabelFrame(self.myframe, text="AST_VIEW")
        self.window_frame.grid(column=2, row=3, padx=100, pady=100)
        f = open(outfile, "r")
        content = f.read()
        f.close()
        self.newlabel = ttk.Label(self.window_frame, text=content)
        self.newlabel.grid(column=3, row=2)
        self.myentry = ttk.Entry(self.myframe, textvariable="blabla", state='readonly')
        self.myscroll = ttk.Scrollbar(self.myframe, orient='horizontal', command=self.myentry.xview)
        self.myentry.config(xscrollcommand=self.myscroll.set)

        self.myframe.grid()
        self.myentry.grid(row=1, sticky='ew')
        self.myscroll.grid(row=2, sticky='ew')

root = Root()
root.mainloop()

