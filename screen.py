import tkinter as tk
import cv2
import numpy as np
import datetime
import threading
from PIL import ImageGrab


root = tk.Tk()
root.geometry('500x200')
root.resizable(False, False)
root.configure(bg="gray")


Target = 'screen'
output_file = 'screen_record.avi'
out = None  # Variable to hold the VideoWriter object

# Function display and reset time
def Display_T():
    global Recorded, Secs, Mins, Hrs
    if Recorded:
        if Secs == 60:
            Secs = 0
            Mins += 1
        elif Mins == 60:
            Mins = 0
            Hrs += 1

        TimeCounter_Label.config(text=str(Hrs) + ':' + str(Mins) + ':' + str(Secs))
        Secs += 1
        TimeCounter_Label.after(1000, Display_T)

def Resetting_T():
    global Secs, Mins, Hrs
    Secs = 0
    Mins = 0
    Hrs = 0

    Target == 'screen'


# Function to start recording

def Starts_Recording():
    global Recorded
    Recorded = not Recorded
    Resetting_T()

    Button_Rec_thread = threading.Thread(target=Recording)
    Thread_Counter = threading.Thread(target=Display_T)
    Thread_Screen = threading.Thread(target=Screen_Recording)

    if Recorded:
        Button_Rec_thread.start()
        Thread_Counter.start()
    if Target == 'screen':
        Thread_Screen.start()


# Function for screen recording
Recorded = False
Target = 'screen'
Show_Preview = True

def Screen_Recording():
    global Show_Preview, Recorded
    name = 'screen'
    Now = datetime.datetime.now()
    date = Now.strftime("%H%M%S")
    FileFormat = 'mp4'
    filename = name + str(date) + '.' + FileFormat
    FeetPerSec = 24
    Resolutions = (1366, 768)
    Thumb_Resolutions = (342, 192)

    Four_Char_Code = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, Four_Char_Code, FeetPerSec, Resolutions)

    while True:
        IMG = ImageGrab.grab()
        np_IMG = np.array(IMG)
        frame = cv2.cvtColor(np_IMG, cv2.COLOR_BGR2RGB)
        writer.write(frame)
        if Show_Preview:
            Thumb = cv2.resize(frame, dsize=Thumb_Resolutions)
            cv2.imshow('Preview - Screen Recorder', Thumb)
        if cv2.waitKey(1) == 27:
            Recorded = False
            label['text'] = 'Video was saved as ' + filename
            Recording()
            break

    writer.release()
    cv2.destroyAllWindows()

# Function for recording button
def Recording():
    global Recorded
    if Recorded:
        recb['state'] = tk.DISABLED
        label['text'] = 'Press ESC to quit.'
    else:
        recb['state'] = tk.NORMAL


TimeCounter_Label = tk.Label(root, text='0:0:0',font=("Times new roman",18,"bold"), bg='gray', fg='white')
TimeCounter_Label.place(x=200, y=100)


recb = tk.Button(root, text="REC", width=20, height=2, command=Starts_Recording)
recb.place(x=180, y=50)
label = tk.Label(root, bg="gray")
label.place(x=180, y=5)

root.mainloop()
