__author__ = 'gumengyuan'

import Tkinter as tk
import tkFileDialog
import os
from Tkinter import *
from gs import GSOperations
from s3 import S3Operations


def get_window(master, ratio_x, ratio_y):
    SCREEN_SIZE_X = master.winfo_screenwidth()
    SCREEN_SIZE_Y = master.winfo_screenheight()
    FrameSizeX  = int(SCREEN_SIZE_X * ratio_x)
    FrameSizeY  = int(SCREEN_SIZE_Y * ratio_y)
    FramePosX   = (SCREEN_SIZE_X - FrameSizeX)/2 # Find left and up border of window
    FramePosY   = (SCREEN_SIZE_Y - FrameSizeY)/2
    return FramePosX, FramePosY, FrameSizeX, FrameSizeY

class ListObjectView(tk.Frame):
    def __init__(self, master, height, width, bucket):
        tk.Frame.__init__(self)
        self.height = height
        self.width = width
        self.master = master
        self.bucket = bucket
        self.reset()

    def reset(self):
        self.objects = []
        self.vars = []
        self.frame = Frame(self.master)
        self.pane_buttons = Frame(self.frame)
        self.button_upload = Button(self.pane_buttons, text="Upload File", command=lambda: self.upload())
        self.button_download = Button(self.pane_buttons, text="Download File", command=lambda: self.download())
        self.button_move = Button(self.pane_buttons, text=self.btn_move, command=lambda: self.move_choose_bucket())

        self.button_delete = Button(self.pane_buttons, text="Delete File", command=lambda: self.delete())

    def draw(self):
        self.frame.destroy()
        self.reset()

        self.frame.place(x=0, y=0, height=self.height, width=self.width)

        label_schema = Label(self.frame, text=self.schema)
        label_schema.pack()

        pane_objects = Frame(self.frame)
        pane_objects.pack(fill="x")
        label_objects = Label(pane_objects, text="%s >> All files:" % self.bucket.name)
        label_objects.pack(side="left")

        self.pane_buttons.pack(fill="x")
        self.button_delete.pack(side="right")
        self.button_upload.pack(side="left")
        self.button_download.pack(side="left")
        self.button_move.pack(side="left")

        self.frame.lift()

        self.objects = self.my_op.list_object(self.bucket)

        self.v = IntVar()
        self.v.set(-1)
        i = 0
        for object in self.objects:
            line_pane = Frame(self.frame)
            line_pane.pack(fill="x", pady=3)

            line_pane = Frame(self.frame)
            line_pane.pack(fill="x")

            var = tk.IntVar()
            cb = Checkbutton(line_pane, variable=var)
            cb.pack(side="left")
            self.vars.append(var)

            Radiobutton(line_pane, text=object.name, variable=self.v, value=i).pack(anchor=W)
            #label_object = Label(line_pane, text="* %s" % object.name)
            #label_object.pack(side="left")
            i += 1

    def delete(self):
        flag = False
        try:
            for index, var in enumerate(self.vars):
                if var.get() == 1:
                    flag = True
                    object = self.objects[index]
                    self.my_op.remove_object(self.bucket, object)
        except:
            msg = 'Fail to remove files.'
            self.draw_top_result(msg)
        else:
            msg = 'Successfully delete all the files chosen.'
            self.draw_top_result(msg)

        if flag == False:
            self.nothing_choosen("Nothing is chosen to be deleted!")

        self.draw()

    def upload(self):
        file = tkFileDialog.askopenfile(parent=self.master, title='Choose a file')
        if file != None:
            data = file.read()
            file.close()
            file_path = file.name
            directory = os.path.split(file_path)[0]
            file_name = os.path.split(file_path)[1]
            print 'Chosen directory: "%s"' % directory
            print 'Chosen filename: "%s"' % file_name
            msg = self.my_op.upload_object(self.bucket, directory, file_name)

            self.draw_top_result(msg)

    def download(self):
        dir = tkFileDialog.askdirectory(initialdir=None, parent=self.master, title='Choose the downloading directory:')
        print dir
        if dir != "":
            msg = self.my_op.download_object(self.bucket, self.objects[self.v.get()].name, dir)

            self.draw_top_result(msg)

    def move(self, bucket_to, top):
        top.destroy()

        print 'move to: %s' % bucket_to.name
        flag = False
        try:
            for index, var in enumerate(self.vars):
                if var.get() == 1:
                    flag = True
                    object = self.objects[index]
                    self.my_op.move_object(self.bucket, bucket_to, object)
        except:
            msg = 'Fail to remove files.'
            self.draw_top_result(msg)
        else:
            msg = 'Successfully move all the files chosen.'
            self.draw_top_result(msg)

        if flag == False:
            self.nothing_choosen("Nothing is chosen to move!")

        self.draw()

    def move_choose_bucket(self):
        pos_x, pos_y, size_x, size_y = get_window(self, 0.4, 0.2)
        top = Toplevel()
        top.geometry("%sx%s+%s+%s" % (size_x, size_y, pos_x, pos_y))
        top.config(padx=10, pady=5)


        buckets = self.other_op.list_bucket()
        v = IntVar()
        v.set(-1)
        i = 0
        for bucket in buckets:
            #self.buckets.append(bucket)
            Radiobutton(top, text=bucket.name, variable=v, value=i).pack(anchor=W)
            i += 1

        button_ok = Button(top, text="Ok", command=lambda: self.move(buckets[v.get()], top))
        button_ok.pack(side="right")
        button_ok = Button(top, text="Cancel", command=lambda: top.destroy())
        button_ok.pack(side="right")

    def top_refresh(self, top):
        top.destroy()
        self.draw()

    def nothing_choosen(self, msg):
        pos_x, pos_y, size_x, size_y = get_window(self, 0.2, 0.1)
        top_nothing = Toplevel()
        top_nothing.geometry("%sx%s+%s+%s" % (size_x, size_y, pos_x, pos_y))
        top_nothing.config(padx=10, pady=5)
        pane_msg = Frame(top_nothing)
        pane_msg.pack(fill="x")
        label_msg = Label(pane_msg, text=msg)
        label_msg.pack(side="left")
        button_ok = Button(top_nothing, text="Ok", command=lambda: top_nothing.destroy())
        button_ok.pack(side="right")

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

class ListObjectViewGS(ListObjectView):

    def __init__(self, master, height, width, bucket):
        self.schema = "Google Cloud"
        self.btn_move = "Move to S3"
        self.my_op = GSOperations
        self.other_op = S3Operations
        ListObjectView.__init__(self, master, height, width, bucket)

    def reset(self):
        ListObjectView.reset(self)

    def draw(self):
        ListObjectView.draw(self)

    def upload(self):
        ListObjectView.upload(self)

    def download(self):
        ListObjectView.download(self)

    # def move(self):
    #     ListObjectView.move(self)

    def delete(self):
        ListObjectView.delete(self)




class ListObjectViewS3(ListObjectView):

    def __init__(self, master, height, width, bucket):
        self.schema = "Amazon S3"
        self.btn_move = "Move to GS"
        self.my_op = S3Operations
        self.other_op = GSOperations
        ListObjectView.__init__(self, master, height, width, bucket)

    def reset(self):
        ListObjectView.reset(self)

    def draw(self):
        ListObjectView.draw(self)

    def upload(self):
        ListObjectView.upload(self)

    def download(self):
        ListObjectView.download(self)

    # def move(self):
    #     ListObjectView.move(self)

    def delete(self):
        ListObjectView.delete(self)