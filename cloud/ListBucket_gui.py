__author__ = 'gumengyuan'

import Tkinter as tk
from Tkinter import *
import s3
import HyperlinkManager
import connection
from gs import GSOperations
from s3 import S3Operations
from ListObject_gui import *
gsOrS3=''

def get_window(master, ratio_x, ratio_y):
    SCREEN_SIZE_X = master.winfo_screenwidth()
    SCREEN_SIZE_Y = master.winfo_screenheight()
    FrameSizeX  = int(SCREEN_SIZE_X * ratio_x)
    FrameSizeY  = int(SCREEN_SIZE_Y * ratio_y)
    FramePosX   = (SCREEN_SIZE_X - FrameSizeX)/2 # Find left and up border of window
    FramePosY   = (SCREEN_SIZE_Y - FrameSizeY)/2
    return FramePosX, FramePosY, FrameSizeX, FrameSizeY

class ListBucketView(tk.Frame):
    def __init__(self, master, height, width):
        tk.Frame.__init__(self)
        self.master = master
        self.height = height
        self.width = width
        self.reset()

    def reset(self):
        self.vars = []
        self.buckets = []
        self.frame = Frame(self.master)
        self.pane_buttons = Frame(self.frame)
        self.button_new = Button(self.pane_buttons, text="New Bucket", command=lambda: self.new())
        self.button_delete = Button(self.pane_buttons, text="Delete Bucket", command=lambda: self.delete())
        #self.scrollbar = Scrollbar(self.frame)
        #self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set)

    def draw(self, op):
        self.frame.destroy()
        self.reset()

        self.frame.place(x=0, y=0, height=self.height, width=self.width)

        #pane_schema = Frame(self.frame)
        #pane_schema.pack(fill="x")
        label_schema = Label(self.frame, text=self.schema)
        label_schema.pack()

        pane_buckets = Frame(self.frame)
        pane_buckets.pack(fill="x")
        label_buckets = Label(pane_buckets, text="All buckets:")
        label_buckets.pack(side="left")

        self.pane_buttons.pack(fill="x")
        self.button_delete.pack(side="right")
        self.button_new.pack(side="right")
        #self.scrollbar.pack(side=RIGHT, fill=Y)


        buckets = op.list_bucket()

        for bucket in buckets:
            self.buckets.append(bucket)
            if self.schema == "Google Cloud":
                obj_view = ListObjectViewGS(self.master, self.height, self.width, bucket)
            elif self.schema == "Amazon S3":
                obj_view = ListObjectViewS3(self.master, self.height, self.width, bucket)



            line_pane = Frame(self.frame)
            line_pane.pack(fill="x")
            #self.listbox.insert(END, "hi")

            var = tk.IntVar()
            cb = Checkbutton(line_pane, variable=var)
            cb.pack(side="left")
            self.vars.append(var)
            #self.check_manager.add(cb)
            text_bucket = Text(line_pane, wrap=CHAR, height=1)
            text_bucket.pack()
            #text_bucket.insert(INSERT, "Hi!")
            hyperlink = HyperlinkManager.HyperlinkManager(text_bucket)
            text_bucket.insert(INSERT, bucket.name, hyperlink.add(obj_view.draw))

        #self.listbox.pack()

        #self.scrollbar.config(command=self.listbox.yview)
        self.frame.lift()

    def delete(self, op):
        flag = False
        try:
            for index, var in enumerate(self.vars):
                if var.get() == 1:
                    flag = True
                    bucket = self.buckets[index]
                    op.remove_bucket(bucket)
        except:
            msg = 'Sorry, but fail to these buckets! '
            self.draw_top_result(msg)
        else:
            msg = 'Successfully remove these buckets and all the objects inside.'
            self.draw_top_result(msg)

        if flag == False:
            pos_x, pos_y, size_x, size_y = get_window(self, 0.2, 0.1)
            top_nothing = Toplevel()
            top_nothing.geometry("%sx%s+%s+%s" % (size_x, size_y, pos_x, pos_y))
            top_nothing.config(padx=10, pady=5)
            pane_msg = Frame(top_nothing)
            pane_msg.pack(fill="x")
            label_msg = Label(pane_msg, text="Nothing is chosen to be deleted!")
            label_msg.pack(side="left")
            button_ok = Button(top_nothing, text="Ok", command=lambda: top_nothing.destroy())
            button_ok.pack(side="right")

        self.draw()

    def new(self, op):
        pos_x, pos_y, size_x, size_y = get_window(self, 0.3, 0.13)
        top = Toplevel()
        top.title("Create New Bucket")
        top.geometry("%sx%s+%s+%s" % (size_x, size_y, pos_x, pos_y))
        top.config(padx=10, pady=5)

        pane_msg = Frame(top)
        pane_msg.pack(fill="x")
        pane_input = Frame(top)
        pane_input.pack(fill="x")
        label_msg = Label(pane_msg, text="Input the name of the new bucket: ")
        label_msg.pack(side="left")

        new_bucket = StringVar()
        entry_input = Entry(pane_input, textvariable=new_bucket)
        entry_input.pack(fill="x")

        button_ok = Button(top, text="ok", command=lambda: self._new(top, new_bucket.get()))
        button_ok.pack(side="right")
        button_cancel = Button(top, text="cancel", command=lambda: top.destroy())
        button_cancel.pack(side="right")

    def _new(self, top, bucket_name, op):
        top.destroy()
        msg = op.make_bucket(bucket_name)

        pos_x, pos_y, size_x, size_y = get_window(self, 0.3, 0.2)
        top = Toplevel()
        top.geometry("%sx%s+%s+%s" % (size_x, size_y, pos_x, pos_y))
        top.config(padx=5, pady=5)
        pane_msg = Frame(top)
        pane_msg.pack(fill="x")
        label_msg = Label(pane_msg, text=msg)
        label_msg.pack(side="left")
        button_ok = Button(top, text="Ok", command=lambda: self.top_refresh(top))
        button_ok.pack(side="right")

    def refresh(self):
        self.frame.destroy()
        self.reset()
        self.draw()

    def top_refresh(self, top):
        top.destroy()
        self.draw()

    def draw_top_result(self, msg):
        pos_x, pos_y, size_x, size_y = get_window(self, 0.4, 0.15)
        top = Toplevel()
        top.geometry("%sx%s+%s+%s" % (size_x, size_y, pos_x, pos_y))
        top.config(padx=10, pady=5)
        pane_msg = Frame(top)
        pane_msg.pack(fill="x")
        label_msg = Label(pane_msg, text=msg)
        label_msg.pack(side="left")
        button_ok = Button(top, text="Ok", command=lambda: self.top_refresh(top))
        button_ok.pack(side="right")

    def draw_null_bucket(self, msg):
        label_msg = Label(self.frame, text='Cannot access %s. Please check your credentials in %s.' % (msg, msg))
        label_msg.pack(fill="both", expand=True)
        self.frame.lift()


class ListBucketViewGS(ListBucketView):

    def __init__(self, master, height, width):
        ListBucketView.__init__(self, master, height, width)
        self.schema = "Google Cloud"

    def myCallback(self):
        for var in self.vars:
            print var.get()

    def draw(self):
        gsOrS3='gs'
        ListBucketView.draw(self, GSOperations)

    def delete(self):
        ListBucketView.delete(self, GSOperations)

    def new(self):
        ListBucketView.new(self, GSOperations)

    def _new(self, top, bucket_name):
        ListBucketView._new(self, top, bucket_name, GSOperations)










class ListBucketViewS3(ListBucketView):

    def __init__(self, master, height, width):
        ListBucketView.__init__(self, master, height, width)
        self.schema = "Amazon S3"

    def draw(self):
        if connection.connect() != '':
            ListBucketView.draw(self, S3Operations)
        else:
            ListBucketView.draw_null_bucket(self, self.schema)



    def delete(self):
        ListBucketView.delete(self, S3Operations)

    def new(self):
        ListBucketView.new(self, S3Operations)


    def _new(self, top, bucket_name):
        ListBucketView._new(self, top, bucket_name, S3Operations)