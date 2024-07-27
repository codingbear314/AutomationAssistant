import mediapipe as mp
import cv2
import time
import math
import pygetwindow as gw
from pywinauto import Desktop
import tkinter as tk
import threading
import pyautogui

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Make pause to 0
pyautogui.PAUSE = 0

Camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

class Pointer:
    def __init__(self, initial_x=0, initial_y=0, diameter=50, color='red'):
        #Create a transparent window
        self.window = tk.Tk()
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.attributes('-transparentcolor', self.window['bg'])
        self.window.attributes('-topmost', True)  # Keep window on top

        #Initial settings
        self.diameter = diameter
        self.color = color

        #Create canvas and dot
        self.canvas = tk.Canvas(self.window, width=self.diameter, height=self.diameter, 
                               highlightthickness=0, bd=0)
        self.dot = self.canvas.create_oval(0, 0, self.diameter, self.diameter, 
                                          fill=self.color, outline=self.color)
        self.canvas.pack()
        self.Xpos = initial_x
        self.Ypos = initial_y
        self.gotoXY(initial_x, initial_y)

    def gotoXY(self, x, y):
        self.Xpos = int(x)
        self.Ypos = int(y)
        x, y = self.Xpos, self.Ypos
        self.window.geometry(f"+{x}+{y}")
    def refresh(self):
        self.Xpos = pyautogui.position().x
        self.Ypos = pyautogui.position().y
        self.gotoXY(self.Xpos, self.Ypos)

    def tick(self):
        if self.Xpos < 0:
            self.Xpos = 0
        if self.Ypos < 0:
            self.Ypos = 0
        if self.Xpos > 2250:
            self.Xpos = 2250
        if self.Ypos > 1480:
            self.Ypos = 1480
        self.Xpos = (self.Xpos)
        self.Ypos = (self.Ypos)
        self.gotoXY(self.Xpos, self.Ypos)

    # def hide(self):
    #     self.window.withdraw()

    # def show(self):
    #     self.window.deiconify()

    # def change_diameter(self, new_diameter):
    #     self.diameter = new_diameter
    #     self.canvas.config(width=self.diameter, height=self.diameter)
    #     self.canvas.coords(self.dot, 0, 0, self.diameter, self.diameter)

    # def change_color(self, new_color):
    #     self.color = new_color
    #     self.canvas.itemconfig(self.dot, fill=self.color, outline=self.color)

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z
    def cross(self, vector):
        return Vector(self.y * vector.z - self.z * vector.y, self.z * vector.x - self.x * vector.z, self.x * vector.y - self.y * vector.x)

def FingerClosed(landmarkFirst, landmarkSecond, landmarkThird, landmarkFourth):
    FirstSection = Vector(landmarkSecond.x - landmarkFirst.x, landmarkSecond.y - landmarkFirst.y, landmarkSecond.z - landmarkFirst.z)
    SecondSection = Vector(landmarkThird.x - landmarkSecond.x, landmarkThird.y - landmarkSecond.y, landmarkThird.z - landmarkSecond.z)
    ThirdSection = Vector(landmarkFourth.x - landmarkThird.x, landmarkFourth.y - landmarkThird.y, landmarkFourth.z - landmarkThird.z)

    # First, let's just calculate the angle between second and first section. We'll use the dot product for this.
    CrossProduct = FirstSection.dot(SecondSection)
    # The size of the dot product is A*B*cos(theta)
    FirstSize = (FirstSection.dot(FirstSection))**0.5
    SecondSize = (SecondSection.dot(SecondSection))**0.5
    CosTheta = CrossProduct / (FirstSize * SecondSize)
    Theta = math.acos(CosTheta)
    # The Theta is expressed in radians. Let's convert it to degrees.
    Theta = math.degrees(Theta)
    
    # If the angle is more than 50 degrees, the finger is possibly closed.
    # print(Theta)
    return Theta > 50

def Point3Angle(FirstPoint, SecondPoint, ThirdPoint):
    FirstSection = Vector(FirstPoint.x - SecondPoint.x, FirstPoint.y - SecondPoint.y, FirstPoint.z - SecondPoint.z)
    SecondSection = Vector(ThirdPoint.x - SecondPoint.x, ThirdPoint.y - SecondPoint.y, ThirdPoint.z - SecondPoint.z)
    # print(FirstSection.x, FirstSection.y, FirstSection.z)
    # print(SecondSection.x, SecondSection.y, SecondSection.z)
    DotProduct = FirstSection.dot(SecondSection)
    FirstSize = (FirstSection.dot(FirstSection))**0.5
    SecondSize = (SecondSection.dot(SecondSection))**0.5
    CosTheta = DotProduct / (FirstSize * SecondSize)
    Theta = math.acos(CosTheta)
    Theta = math.degrees(Theta)
    return Theta

WaitingTabout = False

TabX = -1
TabY = -1
StartX = -1
StartY = -1
StartTime = time.time()

Dot = Pointer(initial_x=900, initial_y=600, diameter=20)
Scale = 4000

def video_capture_loop():
    global WaitingTabout, TabX, TabY, StartX, StartY
    while Camera.isOpened():
        success, image = Camera.read()
        if not success:
            break

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(21):
                    cv2.circle(image, (int(hand_landmarks.landmark[i].x * 640), int(hand_landmarks.landmark[i].y * 480)), 5, (0, 0, 255), -1)

        cv2.imshow('Hand Tracking', image)
        if results.multi_hand_landmarks:
            FirstHand = results.multi_hand_landmarks[0]
            FinClosedSt = lambda first, second, third, fourth : FingerClosed(FirstHand.landmark[first], FirstHand.landmark[second], FirstHand.landmark[third], FirstHand.landmark[fourth])
            
            ThumbOpened = not FinClosedSt(1, 2, 3, 4)
            IndexOpened = not FinClosedSt(5, 6, 7, 8)
            MiddleClosed = FinClosedSt(9, 10, 11, 12)
            RingClosed = FinClosedSt(13, 14, 15, 16)
            PinkyClosed = FinClosedSt(17, 18, 19, 20)

            Angle_IndexEnd_Palm_ThumbEnd = Point3Angle(FirstHand.landmark[4], FirstHand.landmark[0], FirstHand.landmark[8])

            if not WaitingTabout and ThumbOpened and IndexOpened and MiddleClosed and RingClosed and PinkyClosed and Angle_IndexEnd_Palm_ThumbEnd < 5:
                print("Tap!")
                TabX = (FirstHand.landmark[8].x + FirstHand.landmark[4].x)/2
                TabY = (FirstHand.landmark[8].y + FirstHand.landmark[4].y)/2
                StartX = Dot.Xpos
                StartY = Dot.Ypos
                StartTime = time.time()
                WaitingTabout = True
            elif WaitingTabout and not (Angle_IndexEnd_Palm_ThumbEnd < 15):
                print("Tabout!")
                if time.time()-StartTime < 0.4:
                    #Click!
                    print("Click!")
                    Dot.Xpos = StartX
                    Dot.Ypos = StartY
                    Dot.tick()
                    try:
                        OP = pyautogui.position()
                        pyautogui.moveTo(Dot.Xpos, Dot.Ypos)
                        pyautogui.click()
                        pyautogui.moveTo(OP)
                    except:
                        print("Can't click, it's out of bounds!")
                WaitingTabout = False
            elif WaitingTabout:
                GetX = (FirstHand.landmark[8].x + FirstHand.landmark[4].x)/2
                GetY = (FirstHand.landmark[8].y + FirstHand.landmark[4].y)/2
                Dot.Xpos = StartX + (GetX - TabX) * Scale
                Dot.Ypos = StartY + (GetY - TabY) * Scale
                Dot.tick()

        if cv2.waitKey(8) & 0xFF == 27:
            break

    Camera.release()
    cv2.destroyAllWindows()

# Run the video capture loop in a separate thread
video_thread = threading.Thread(target=video_capture_loop)
video_thread.start()

# Run the Tkinter main loop in the main thread
Dot.window.mainloop()