__author__ = 'gumengyuan'

import Tkinter as tk
from Tkinter import *
from ListBucket_gui import *
#from main import App


class MainView(tk.Frame):
    def __init__(self, width, height):
        tk.Frame.__init__(self)
        self.width = width
        self.height = height

    def show(self):
        self.lift()

    def draw(self, master, parent):
        self.place(in_=master, x=0, y=0, height=self.height, width=self.width)
        self.parent = parent
        #self.grid_columnconfigure(1, weight=1)

        #split the mainview into two part:
        #   left_pane: change to different storage
        #   right_pane: main view in different storage
        padding = 10
        left_pane = Frame(self, bd=1, relief=SUNKEN, padx=padding, pady=padding)
        right_pane = Frame(self, bd=1, relief=SUNKEN, padx=padding, pady=padding)
        split = 0.25
        left_pane.place(relx=0, relheight=1, relwidth=split)
        right_pane.place(relx=split, relheight=1, relwidth=1.0-split)

        gs_view = ListBucketViewGS(right_pane, self.height-2*padding, (1.0-split)*self.width-2*padding)
        s3_view = ListBucketViewS3(right_pane, self.height-2*padding, (1.0-split)*self.width-2*padding)
        #login_view = App(self.master)

        label_goto = Label(left_pane, text="Go to: ")
        button_gs = Button(left_pane, text="Google Cloud", fg="yellow", command=lambda: gs_view.draw())
        button_amazon = Button(left_pane, text="Amazon S3", fg="red", command=lambda: s3_view.draw())
        button_rtc = Button(left_pane, text="WebRTC", fg="blue")

        button_exit = Button(left_pane, text="Logout", command=lambda: self.logout())

        label_goto.pack(fill=X)
        button_gs.pack(fill=X)
        button_amazon.pack(fill=X)
        button_rtc.pack(fill=X)
        button_exit.pack(side="bottom", fill=X)

        label_occ = Label(right_pane, text="Nothing here..")
        label_occ.pack(fill="both", expand=True)

    def logout(self):
        self.destroy()
        self.parent.draw()


