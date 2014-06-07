__author__ = 'gumengyuan'


from main_gui import MainView
from gs import GSOperations
from Tkinter import *
import connection
import os

crendential_file = 'credential_s3.txt'

class App:

    def __init__(self, master):
        # Define frame size and position in the screen :
        self.master = master
        FramePosX, FramePosY, FrameSizeX, FrameSizeY, = App.get_window(self.master, 0.6, 0.6)  # Get screen width and height [pixels]
        self.master.geometry("%sx%s+%s+%s"%(FrameSizeX,FrameSizeY,FramePosX,FramePosY))
        self.master.protocol('WM_DELETE_WINDOW', self.handler_exit)
        self.FrameSizeX = FrameSizeX
        self.FrameSizeY = FrameSizeY
        self.frame = Frame(self.master)
        self.draw()


    def reset(self):
        self.frame = Frame(self.master)


        self.label1 = Label(self.frame, text="Welcome to Cloud Storage & Transmission", pady=40, font=("Purisa",18))
        self.label2 = Label(self.frame, text="Management System!", font=("Purisa",18))


        self.pane_main = Frame(self.frame, padx=40, pady=40)

        self.access_key = StringVar()
        self.secret_key = StringVar()
        self.remember = IntVar()
        self.btn_enter = Button(self.frame, text="Enter", command=lambda: self.enter_main_frame(self.master, self.FrameSizeX, self.FrameSizeY))

    def draw(self):
        self.frame.destroy()
        self.reset()

        self.frame.pack(fill="both", expand=True)
        self.label1.pack(side="top", fill="x")
        self.label2.pack(side="top", fill="x")
        self.pane_main.pack(fill="x")

        self.draw_main_pane(self.pane_main)

        self.btn_enter.pack(side="right", padx=50)
        self.frame.lift()

    def say_hi(self):
        print "hello !"

    def handler_exit(self):
        self.master.destroy()
        print "Destroy root window."
        self.master.quit()
        print "Quit main loop."

    def enter_main_frame(self, master, size_x, size_y):
        if (self.access_key.get() == '') or (self.secret_key.get() == ''):
            pass

        s3_access_key = self.access_key.get()
        s3_secret_key = self.secret_key.get()

        #print 'access: %s' % s3_access_key
        #print 'secret: %s' % s3_secret_key
        connection.setCredentials(s3_access_key, s3_secret_key)

        if self.remember.get() == 0:
            delete_credentials()
        else:
            save_credentials(s3_access_key, s3_secret_key)



        main_view = MainView(size_x, size_y)
        main_view.draw(master, self)


    def draw_main_pane(self, master):
        pane_line1 = Frame(master, padx=10, pady=20)
        pane_line1.pack(fill="x")

        keys = get_credentials()
        if keys != []:
            self.access_key.set(keys[0])
            self.secret_key.set(keys[1])
            self.remember.set(1)

        label_access = Label(pane_line1, text="Amazon S3 Access Key: ")
        label_access.pack(side="left")
        entry_access = Entry(pane_line1, textvariable=self.access_key)
        entry_access.pack(fill="x")

        pane_line2 = Frame(master, padx=10, pady=20)
        pane_line2.pack(fill="x")
        label_secret = Label(pane_line2, text="Amazon S3 Secret Key: ")
        label_secret.pack(side="left")
        entry_secret = Entry(pane_line2, textvariable=self.secret_key, show="*")
        entry_secret.pack(fill="x")


        cb = Checkbutton(master, text="remember", variable=self.remember, pady = 10)
        cb.pack(side="left")


    @staticmethod
    def get_window(master, ratio_x, ratio_y):
        SCREEN_SIZE_X = master.winfo_screenwidth()
        SCREEN_SIZE_Y = master.winfo_screenheight()
        FrameSizeX  = int(SCREEN_SIZE_X * ratio_x)
        FrameSizeY  = int(SCREEN_SIZE_Y * ratio_y)
        FramePosX   = (SCREEN_SIZE_X - FrameSizeX)/2 # Find left and up border of window
        FramePosY   = (SCREEN_SIZE_Y - FrameSizeY)/2
        return FramePosX, FramePosY, FrameSizeX, FrameSizeY

def delete_credentials():
    if os.path.isfile(crendential_file):
        os.remove(crendential_file)

def save_credentials(accessKey, secretKey):
    try:
        file = open(crendential_file, "w")
        file.write("[Credentials]\n")
        file.write("aws_access_key_id="+accessKey+"\n")
        file.write("aws_secret_access_key="+secretKey+"\n")
        file.close()
    except:
        return "Failed to store Credentials."

def get_credentials():

    try:
        file = open(crendential_file, 'r')
        keys=[] #use keys.append
        file.readline()
        taggedAccessKey=file.readline()
        taggedSecretKey=file.readline()
        keys.append(taggedAccessKey.split('=', 1)[1].strip())
        keys.append(taggedSecretKey.split('=', 1)[1].strip())
    except:
        return []
    else:
        return keys

def main():
    print '[This is Google Cloud Storage]'
    print ''

    root = Tk()
    root.title("Cloud Storage & Transmission")

    app = App(root)

    root.mainloop()

    op = GSOperations()
    mode = ""

    # while mode!="q":
    #     mode = raw_input("Select your operation in mb, lb, lo, rb, ro, uo, do. (Exit: q.):\n")
    #     if mode == "mb":
    #         op.make_bucket()
    #     elif mode == "lb":
    #         op.list_bucket()
    #     elif mode == "lo":
    #         op.list_object()
    #     elif mode == "rb":
    #         op.remove_bucket()
    #     elif mode == "ro":
    #         op.remove_object()
    #     elif mode == "uo":
    #         op.upload_object()
    #     elif mode == "do":
    #         op.download_object()









if __name__ == "__main__":
    main()