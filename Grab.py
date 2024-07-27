import mediapipe as mp
import cv2
import time
import math
import pygetwindow as gw
from pywinauto import Desktop

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

Camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

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
            WaitingTabout = True
        elif WaitingTabout and not (Angle_IndexEnd_Palm_ThumbEnd < 15):
            print("Tabout!")
            WaitingTabout = False
        elif WaitingTabout and not (ThumbOpened and IndexOpened and MiddleClosed and RingClosed and PinkyClosed):
            print("Stopped Tabbing!")
            WaitingTabout = False

    if cv2.waitKey(5) & 0xFF == 27:
        break