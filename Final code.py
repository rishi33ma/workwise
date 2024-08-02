import PySimpleGUI as sg
import tkinter.font as tkFont
from tkinter import filedialog
import os.path
import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import time

hours = -1
minutes = -1
seconds = -1
hours_2 = -1
minutes_2 = -1
seconds_2 = -1

reset = 0

def select_schedule():
    clicked.set(hours)
    clicked2.set(minutes)
    clicked3.set(seconds)
    clicked4.set(hours_2)
    clicked5.set(minutes_2)
    clicked6.set(seconds_2)

def reset_values():
    global reset, sum
    clicked.set(0)
    clicked2.set(0)
    clicked3.set(0)
    clicked4.set(0)
    clicked5.set(0)
    clicked6.set(0)
    sum = 0
    label1.config(text="")
    label01.config(text="")

    reset = 1


def savefileas():
    try:
        path = filedialog.asksaveasfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*"))).name

    except:
        return

    with open(path, 'w') as f:
        f.write("Take a Break in:\n")
        f.write(str(clicked.get()) + "Hrs " + str(clicked2.get()) + "mins " + str(clicked3.get()) + "secs")
        f.write("\nTake a Break for:\n")
        f.write(str(clicked4.get()) + "Hrs " + str(clicked5.get()) + "mins " + str(clicked6.get()) + "secs")



def scheduler():
    global hours, minutes, seconds, hours_2, minutes_2, seconds_2

    # Create the tkinter window
    ws = tk.Tk()
    ws.withdraw()  # Hide the tkinter window

    # Function to open a file
    def openfile():
        if not text_zone.edit_modified():
            try:
                path = filedialog.askopenfile(filetypes=(("Text files", ".txt"), ("All files", ".*"))).name
                window['-TOUT-'].update('Notepad - ' + path)
                with open(path, 'r') as f:
                    content = f.read()
                    text_zone.delete('1.0', tk.END)
                    text_zone.insert('1.0', content)

                    text_zone.edit_modified(0)
            except:
                pass
        else:
            openfile()

    text_zone = sg.Multiline(size=(40, 20), key='-TEXT-')
    file_list_column = [
        [
            sg.Text("Schedule Folder"),
            sg.Input(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(initial_folder='C:/Users/matal/OneDrive/Desktop/VIT -COLLEGE/SY_/sem2/EDI/codes'),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-",
                select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED
            )
        ],
        [
            sg.Button("ADD", key="-ADD_SCHEDULE-")
        ],
    ]

    # For now will only show the name of the file that was chosen
    schedule_viewer_column = [
        [sg.Text("Choose a schedule:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Text(size=(40, 19), key="-TEXT-")],
    ]

    # ----- Full layout -----
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeparator(),
            sg.Column(schedule_viewer_column),
        ]
    ]
    window = sg.Window("Scheduler", layout)

    # Run the Event Loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == '-EXIT-':
            break

        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []
            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith(".txt")
            ]
            window["-FILE LIST-"].update(fnames)

        elif event == "-FILE LIST-":  # A file was chosen from the listbox
            try:
                filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])

                with open(filename, "r") as f:
                    content = f.read()
                    window["-TEXT-"].update(content)

                with open(filename, "r") as f:
                    # content = f.read()
                    # window["-TEXT-"].update(content)
                    k=0
                    line = f.readlines()
                    for i in range(2):
                        l = len(line[(i*2)+1])
                        for j in range(l):

                            if line[(i * 2) + 1][j].isnumeric() and k == 0:
                                # print("this is 1st number", line[(i * 2) + 1][j])
                                if line[(i * 2) + 1][j + 1].isnumeric():
                                    hours = int(line[(i * 2) + 1][j]) * 10 + int(line[(i * 2) + 1][j + 1])
                                    k = k - 1
                                elif line[(i * 2) + 1][j - 1].isnumeric():
                                    k = k + 1
                                    continue
                                else:
                                    hours = int(line[(i * 2) + 1][j])
                                k = k + 1
                                print(hours)

                            elif line[(i * 2) + 1][j].isnumeric() and k == 1:
                                # minutes=int(j)
                                # print("this is 2nd number", line[(i * 2) + 1][j])
                                if line[(i * 2) + 1][j + 1].isnumeric():
                                    minutes = int(line[(i * 2) + 1][j]) * 10 + int(line[(i * 2) + 1][j + 1])
                                    k = k - 1
                                elif line[(i * 2) + 1][j - 1].isnumeric():
                                    k = k + 1
                                    continue
                                else:
                                    minutes = int(line[(i * 2) + 1][j])
                                k = k + 1
                                print(minutes)

                            elif line[(i * 2) + 1][j].isnumeric() and k == 2:
                                # seconds=int(j)
                                # print("this is 3rd number", line[(i * 2) + 1][j])
                                if line[(i * 2) + 1][j + 1].isnumeric():
                                    seconds = int(line[(i * 2) + 1][j]) * 10 + int(line[(i * 2) + 1][j + 1])
                                    # j=j+1
                                    k = k - 1
                                elif line[(i * 2) + 1][j - 1].isnumeric():
                                    k = k + 1
                                    continue
                                else:
                                    seconds = int(line[(i * 2) + 1][j])
                                k = k + 1
                                print(seconds)

                            elif line[(i * 2) + 1][j].isnumeric() and k == 3:
                                # hours_2=int(j)
                                # print("this is 4th number", line[(i * 2) + 1][j])
                                if line[(i * 2) + 1][j + 1].isnumeric():
                                    hours_2 = int(line[(i * 2) + 1][j]) * 10 + int(line[(i * 2) + 1][j + 1])
                                    k = k - 1
                                elif line[(i * 2) + 1][j - 1].isnumeric():
                                    k = k + 1
                                    continue
                                else:
                                    hours_2 = int(line[(i * 2) + 1][j])
                                k = k + 1
                                print(hours_2)

                            elif line[(i * 2) + 1][j].isnumeric() and k == 4:
                                # minutes_2=int(j)
                                # print("this is 5th number", line[(i * 2) + 1][j])
                                if line[(i * 2) + 1][j + 1].isnumeric():
                                    minutes_2 = int(line[(i * 2) + 1][j]) * 10 + int(line[(i * 2) + 1][j + 1])
                                    k = k - 1
                                elif line[(i * 2) + 1][j - 1].isnumeric():
                                    k = k + 1
                                    continue
                                else:
                                    minutes_2 = int(line[(i * 2) + 1][j])
                                k = k + 1
                                print(minutes_2)

                            elif line[(i * 2) + 1][j].isnumeric() and k == 5:
                                # seconds_2=int(j)
                                # print("this is 6th number", line[(i * 2) + 1][j])
                                if line[(i * 2) + 1][j + 1].isnumeric():
                                    seconds_2 = int(line[(i * 2) + 1][j]) * 10 + int(line[(i * 2) + 1][j + 1])
                                    k = k - 1
                                elif line[(i * 2) + 1][j - 1].isnumeric():
                                    k = k + 1
                                    continue
                                else:
                                    seconds_2 = int(line[(i * 2) + 1][j])
                                k = k + 1
                                print(seconds_2)

                            elif line[(i * 2) + 1][j].isspace():
                                continue


            except:
                pass

            window["-FILE LIST-"].update(fnames)

        if event == "-ADD_SCHEDULE-":
            select_schedule()

sum = 0
def freeze_timer(str):
    global sum, tym

    try:
        tym = int(clicked.get()) * 3600 + int(clicked2.get()) * 60 + int(clicked3.get())
    except:
        print("Please Input The Correct Value")
    # while temp > -1:

    Mins, Secs = divmod(temp, 60)
    Hours = 0
    if Mins > 60:
        Hours, Mins = divmod(Mins, 60)

    root.update()


    STR = int(str)
    if STR == 0:
        sum = 0

    sum = sum + STR
    if(tym == sum):
        root_1 = tk.Tk()
        root_1.attributes("-fullscreen", True, "-topmost", True, "-disabled", True)

        time_interrupt = (int(clicked4.get()) * 3600 + int(clicked5.get()) * 60 + int(
            clicked6.get())) * 1000  # Time screen is active in ms
        root_1.after(time_interrupt, root_1.destroy)


root = Tk()
# Adjust size
root.geometry( "700x600" )
root.title("BreakScheduling Software")

def tutorial():
    newWindow2 = Toplevel(root)
    newWindow2.title("Manual")
    newWindow2.geometry("700x600")
    # Create a canvas for displaying the video frames
    canvas1 = tk.Canvas(newWindow2, width=700, height=600)
    canvas1.grid(row=0, column=0)

    # Load the image
    image = Image.open("ex3.png")  # Replace with the path to your image file
    resized_image = image.resize((700, 600))
    # Create a PhotoImage object from the loaded image
    photo = ImageTk.PhotoImage(resized_image)

    # Create a Label widget to display the image
    labell = tk.Label(newWindow2, image=photo)
    labell.grid(row=0, column=0)

def exercise():
    newWindow3 = Toplevel(root)
    newWindow3.title("Exercises")
    newWindow3.geometry("700x600")
    # Create a canvas for displaying the video frames
    canvas2 = tk.Canvas(newWindow3, width=700, height=600)
    canvas2.grid(row=0, column=0)

    # Load the image
    image = Image.open("ex3.png")  # Replace with the path to your image file
    resized_image = image.resize((700, 600))
    # Create a PhotoImage object from the loaded image
    photo = ImageTk.PhotoImage(resized_image)

    # Create a Label widget to display the image
    labell2 = tk.Label(newWindow3, image=photo)
    labell2.grid(row=0, column=0)

def openNewWindow():
    global label, reset
    reset = 0
    newWindow = Toplevel(root)
    newWindow.title("Camera")
    newWindow.geometry("700x600")


    # Create a canvas for displaying the video frames
    canvas = tk.Canvas(newWindow, width=700, height=600)
    canvas.grid(row=0, column=0)

    # Create a label for displaying the video frames
    label = tk.Label(newWindow, width=700, height= 600)
    label.grid(row=0, column=0)

    update_frame()


# Initialize Mediapipe Pose Detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


cap = cv2.VideoCapture(0)
Hour = StringVar()
Minute = StringVar()
Second = StringVar()
Minute.set("2")
left_counter = 0
left_stage = "down"
right_counter = 0
right_stage = "down"
temp = int(Minute.get()) * 60


def ok():
    global temp, left_counter, right_counter

    while temp > -1:

        root.update()
        if reset == 1:
            return
        time.sleep(0.2)
        temp -= 1

        try:
            if (temp == 0 and left_counter <5  and right_counter <5):
                messagebox.showinfo("Shoulder Movement", "You haven't moved your shoulders since last 30 mins.\n Please raise your hands for 5 times at least. ")
                freeze_timer("30")
                temp = int(Minute.get()) * 60

            if(temp ==0):
                temp = int(Minute.get()) * 60

        except:
            pass





# Function to update the video frames in the GUI
def update_frame():
    global left_counter, left_stage, right_counter, right_stage, temp

    ret, frame = cap.read()
    if ret:
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with Mediapipe Pose Detection
        results = pose.process(frame_rgb)
        # landmarks = results.pose_landmarks.landmark
        # Draw the pose landmark on the frame
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame_rgb, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            # Get coordinates
            left_ear = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR.value].x,
                        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR.value].y]
            left_shoulder = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

            # Calculate angle
            left_angle = calculate_angle(left_ear, left_shoulder, left_elbow)

            # Visualize angle
            cv2.putText(frame, str(left_angle),
                        tuple(np.multiply(left_shoulder, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            # Curl counter logic
            if left_angle > 160:
                left_stage = "down"
            if left_angle < 100 and left_stage == 'down':
                left_stage = "up"
                left_counter += 1
                print(left_counter)

                # Get coordinates
            right_ear = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR.value].x,
                         results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
            right_shoulder = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            # Calculate angle
            right_angle = calculate_angle(right_ear, right_shoulder, right_elbow)

            # Visualize angle
            cv2.putText(frame, str(right_angle),
                        tuple(np.multiply(right_shoulder, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )

            # Curl counter logic
            if right_angle > 160:
                right_stage = "down"
            if right_angle < 100 and right_stage == 'down':
                right_stage = "up"
                right_counter += 1
                print(right_counter)

            cv2.rectangle(frame_rgb, (0, 0), (225, 73), (245, 117, 16), -1)

            # # Rep data
            cv2.putText(frame_rgb, 'REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame_rgb, str(left_counter),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            cv2.putText(frame_rgb, 'STAGE', (65, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            cv2.putText(frame_rgb, left_stage,
                        (60, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # Convert the frame to PIL Image
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Convert the PIL Image to PhotoImage
        frame_tk = ImageTk.PhotoImage(frame_pil)

        # Update the label with the new video frame
        label.config(image=frame_tk)
        label.image = frame_tk

    # Schedule the next frame update after 10ms
    label.after(10, update_frame)
    ok()


# creating a font object
fontObj = tkFont.Font(size=15)
fontObj_head = tkFont.Font(size=28)
fontObj2 = tkFont.Font(size=11)


# label = tk.Label(root, text='BreakScheduling Software\n', compound='center', font=fontObj_head)
# label.grid(column=3, row=0)
label1 = tk.Label(root, text='Take a Break in : ', compound='center', font=fontObj)
label1.grid(column=3, row=1)

# Change the label text
def show():
    label1.config(text = str(clicked.get()) + "Hrs " + str(clicked2.get()) + "mins " + str(clicked3.get()) + "secs")

# Change the label text (second)
def show2():
    label01.config(text = str(clicked4.get()) + "Hrs " + str(clicked5.get()) + "mins " + str(clicked6.get()) + "secs")

# Dropdown menu options
options = [0, 1, 2, 3, 4]
options2 = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50]
options3 = [0, 30]
options4 = [0, 1, 2, 3, 4]
options5 = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50]
options6 = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50]

# datatype of menu text
clicked = IntVar()
clicked2 = IntVar()
clicked3 = IntVar()
clicked4 = IntVar()
clicked5 = IntVar()
clicked6 = IntVar()

# initial menu text
clicked.set(0)
clicked2.set(0)
clicked3.set(0)
clicked4.set(0)
clicked5.set(0)
clicked6.set(0)

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
root.columnconfigure(6, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)
root.rowconfigure(9, weight=1)
root.rowconfigure(10, weight=1)
root.rowconfigure(11, weight=1)
root.rowconfigure(12, weight=1)
root.rowconfigure(13, weight=1)
root.rowconfigure(14, weight=1)

label = tk.Label(root, text='Hours', compound='center', font=fontObj2, fg='blue')
label.grid(column=2, row=2, sticky=tk.E)
label = tk.Label(root, text='Minutes', compound='center', font=fontObj2, fg='blue')
label.grid(column=3, row=2)
label = tk.Label(root, text='Seconds', compound='center', font=fontObj2, fg='blue')
label.grid(column=4, row=2, sticky=tk.W)

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.grid(column=2, row=3, sticky=tk.E)
drop = OptionMenu(root, clicked2, *options2)
drop.grid(column=3, row=3)
drop = OptionMenu(root, clicked3, *options3)
drop.grid(column=4, row=3, sticky=tk.W)

# Create button, it will change label text
button = Button(root, text="Set Time", compound='center', width=15, command=show)
button.grid(column=3, row=4)

# Create Label
label1 = tk.Label(root, text=" ", compound='center', font=fontObj)
label1.grid(column=3, row=5)

label01 = tk.Label(root, text='Take a Break for : ', compound='center', font=fontObj)
label01.grid(column=3, row=6)

label = tk.Label(root, text='Hours', compound='center', font=fontObj2, fg='blue')
label.grid(column=2, row=7, sticky=tk.E)
label = tk.Label(root, text='Minutes', compound='center', font=fontObj2, fg='blue')
label.grid(column=3, row=7)
label = tk.Label(root, text='Seconds', compound='center', font=fontObj2, fg='blue')
label.grid(column=4, row=7, sticky=tk.W)

# Create Dropdown menu2
drop2 = OptionMenu(root, clicked4, *options4)
drop2.grid(column=2, row=8, sticky=tk.E)
drop2 = OptionMenu(root, clicked5, *options5)
drop2.grid(column=3, row=8)
drop2 = OptionMenu(root, clicked6, *options6)
drop2.grid(column=4, row=8, sticky=tk.W)

# Create button, it will change label text
button2 = Button(root, text="Set Time", compound='center',width=15, command=show2)
button2.grid(column=3, row=9)

# Create Label (second)
label01 = tk.Label(root, text=" ", compound='center', font=fontObj)
label01.grid(column=3, row=10)

# add button
button3 = Button(root, text="ADD", compound='left', width=30, command=scheduler)
button3.grid(column=2, row=11)
# save button
button4 = Button(root, text="SET", compound='center', width=30, command=freeze_timer("0"))
button4.grid(column=3, row=11)


button6 = Button(root, text="START MONITORING", compound='left', width=30, command=openNewWindow)
button6.grid(column=2, row=12)
button7 = Button(root, text="SAVE AS", compound='center', width=30, command=savefileas)
button7.grid(column=4, row=11)
button8 = Button(root, text="RESET", compound='right', width=30, command=reset_values)
button8.grid(column=4, row=12)


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Add", command=scheduler)
filemenu.add_command(label="Set", command=freeze_timer("0"))
filemenu.add_command(label="Start Monitoring", command=openNewWindow)
filemenu.add_command(label="Save as...", command=savefileas)
filemenu.add_command(label="Reset", command=reset_values)
filemenu.add_command(label="Exercises", command=exercise)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="User Manual",command=tutorial)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)
root.mainloop()
cap.release()
cv2.destroyAllWindows()
