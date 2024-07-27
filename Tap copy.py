import cv2
import mediapipe as mp
import time
import pygetwindow as gw
from pywinauto import Desktop

demo = gw.getWindowsWithTitle("제목 없음 - 메모장")[-1]

objN = None

import warnings

warnings.filterwarnings("ignore", category=UserWarning)


mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

cap = cv2.VideoCapture(0)  # Use 0 for webcam

Xresolution = 1800
Yresolution = 1200

def BoolToTF(boolean):
    if boolean:
        return "C"
    else:
        return "O"

def FingerClosed(landmarkFirst, landmarkSecond, landmarkThird, landmarkFourth):
    sqrt = lambda x: x**0.5
    D1 = sqrt((landmarkFirst.x - landmarkSecond.x)**2 + (landmarkFirst.y - landmarkSecond.y)**2 + (landmarkFirst.z - landmarkSecond.z)**2)
    D2 = sqrt((landmarkSecond.x - landmarkThird.x)**2 + (landmarkSecond.y - landmarkThird.y)**2 + (landmarkSecond.z - landmarkThird.z)**2)
    D3 = sqrt((landmarkThird.x - landmarkFourth.x)**2 + (landmarkThird.y - landmarkFourth.y)**2 + (landmarkThird.z - landmarkFourth.z)**2)
    FD = sqrt((landmarkFirst.x - landmarkFourth.x)**2 + (landmarkFirst.y - landmarkFourth.y)**2 + (landmarkFirst.z - landmarkFourth.z)**2)

    if D1+D2+D3 > FD*1.4:
        return True
    else:
        return False

def get_window_info():
    # Get all top-level windows
    desktop = Desktop(backend="win32")
    windows = desktop.windows()

    window_info_list = []

    # Iterate over the windows to get the required information
    for depth, window in enumerate(windows):
        if window.is_visible() and window.window_text().strip() and window.window_text() not in ["Program Manager", "Start", "Windows 입력 환경"]:
            name = window.window_text()
            window_id = window.handle
            rect = window.rectangle()
            coordinates = (int(rect.left*1800/2256), int(rect.top*1200/1504))
            size = (int(rect.width()*1800/2256), int(rect.height()*1200/1504))
            window_info_list.append((name, window_id, coordinates, size, depth + 1))

    # Sort the list by depth (which is the last element in the tuple)
    window_info_list.sort(key=lambda x: x[4])

    return window_info_list

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to read image.")
        break
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hand.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks and len(results.multi_hand_landmarks)==2:
        Landmarks1 = results.multi_hand_landmarks[0]
        Landmarks2 = results.multi_hand_landmarks[1]
        Names = ["WRIST", "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP", "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP", "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP", "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP", "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"]
        #for i in range(21):
        #    print(i, Names[i], Landmarks.landmark[i])
        # WRISTX1 = Landmarks1.landmark[0].x
        # WRISTY1 = Landmarks1.landmark[0].y
        # WRISTZ1 = Landmarks1.landmark[0].z
        # THUMBX1 = Landmarks1.landmark[4].x
        # THUMBY1 = Landmarks1.landmark[4].y
        # THUMBZ1 = Landmarks1.landmark[4].z
        INDEXX1 = Landmarks1.landmark[8].x
        INDEXY1 = Landmarks1.landmark[8].y
        # INDEXZ1 = Landmarks1.landmark[8].z
        # MIDDLEX1 =Landmarks1.landmark[12].x
        # MIDDLEY1 =Landmarks1.landmark[12].y
        # MIDDLEZ1 =Landmarks1.landmark[12].z
        # RINGX1  = Landmarks1.landmark[16].x
        # RINGY1  = Landmarks1.landmark[16].y
        # RINGZ1  = Landmarks1.landmark[16].z
        # PINKYX1 = Landmarks1.landmark[20].x
        # PINKYY1 = Landmarks1.landmark[20].y
        # PINKYZ1 = Landmarks1.landmark[20].z

        # WRISTX2 = Landmarks2.landmark[0].x
        # WRISTY2 = Landmarks2.landmark[0].y
        # WRISTZ2 = Landmarks2.landmark[0].z
        # THUMBX2 = Landmarks2.landmark[4].x
        # THUMBY2 = Landmarks2.landmark[4].y
        # THUMBZ2 = Landmarks2.landmark[4].z
        INDEXX2 = Landmarks2.landmark[8].x
        INDEXY2 = Landmarks2.landmark[8].y
        # INDEXZ2 = Landmarks2.landmark[8].z
        # MIDDLEX2 =Landmarks2.landmark[12].x
        # MIDDLEY2 =Landmarks2.landmark[12].y
        # MIDDLEZ2 =Landmarks2.landmark[12].z
        # RINGX2  = Landmarks2.landmark[16].x
        # RINGY2  = Landmarks2.landmark[16].y
        # RINGZ2  = Landmarks2.landmark[16].z
        # PINKYX2 = Landmarks2.landmark[20].x
        # PINKYY2 = Landmarks2.landmark[20].y
        # PINKYZ2 = Landmarks2.landmark[20].z

        # sqrt = lambda x: x**0.5

        # WTD1 = sqrt((WRISTX1 - THUMBX1)**2 + (WRISTY1 - THUMBY1)**2 + (WRISTZ1 - THUMBZ1)**2)
        # WID1 = sqrt((WRISTX1 - INDEXX1)**2 + (WRISTY1 - INDEXY1)**2 + (WRISTZ1 - INDEXZ1)**2)
        # WMD1 = sqrt((WRISTX1 - MIDDLEX1)**2 +(WRISTY1 - MIDDLEY1)**2 +(WRISTZ1 - MIDDLEZ1)**2)
        # WRD1 = sqrt((WRISTX1 - RINGX1)**2 +  (WRISTY1 - RINGY1)**2 +  (WRISTZ1 - RINGZ1)**2)
        # WPD1 = sqrt((WRISTX1 - PINKYX1)**2 + (WRISTY1 - PINKYY1)**2 + (WRISTZ1 - PINKYZ1)**2)

        # WTD2 = sqrt((WRISTX2 - THUMBX2)**2 + (WRISTY2 - THUMBY2)**2 + (WRISTZ2 - THUMBZ2)**2)
        # WID2 = sqrt((WRISTX2 - INDEXX2)**2 + (WRISTY2 - INDEXY2)**2 + (WRISTZ2 - INDEXZ2)**2)
        # WMD2 = sqrt((WRISTX2 - MIDDLEX2)**2 +(WRISTY2 - MIDDLEY2)**2 +(WRISTZ2 - MIDDLEZ2)**2)
        # WRD2 = sqrt((WRISTX2 - RINGX2)**2 +  (WRISTY2 - RINGY2)**2 +  (WRISTZ2 - RINGZ2)**2)
        # WPD2 = sqrt((WRISTX2 - PINKYX2)**2 + (WRISTY2 - PINKYY2)**2 + (WRISTZ2 - PINKYZ2)**2)

        # print(f"Distance between WRIST and THUMB : {WTD}")
        # print(f"Distance between WRIST and INDEX : {WID}")
        # print(f"Distance between WRIST and MIDLE : {WMD}")
        # print(f"Distance between WRIST and RIING : {WRD}")
        # print(f"Distance between WRIST and PINKY : {WPD}")
        # print()


        Pose = [None, None]
        FC1 = lambda l1, l2, l3, l4 : FingerClosed(Landmarks1.landmark[l1], Landmarks1.landmark[l2], Landmarks1.landmark[l3], Landmarks1.landmark[l4])
        FC2 = lambda l1, l2, l3, l4 : FingerClosed(Landmarks2.landmark[l1], Landmarks2.landmark[l2], Landmarks2.landmark[l3], Landmarks2.landmark[l4])
        FCINDEX1 = FC1(5, 6, 7, 8)
        FCINDEX2 = FC2(5, 6, 7, 8)
        FCMIDLE1 = FC1(9, 10, 11, 12)
        FCMIDLE2 = FC2(9, 10, 11, 12)
        FCRING1 = FC1(13, 14, 15, 16)
        FCRING2 = FC2(13, 14, 15, 16)
        FCPINKY1 = FC1(17, 18, 19, 20)
        FCPINKY2 = FC2(17, 18, 19, 20)
        print(f"{BoolToTF(FCINDEX1)}, {BoolToTF(FCMIDLE1)}, {BoolToTF(FCRING1)}\t{BoolToTF(FCPINKY1)}, {BoolToTF(FCINDEX2)}, {BoolToTF(FCMIDLE2)}, {BoolToTF(FCRING2)}, {BoolToTF(FCPINKY2)}")

        if (not FCINDEX1) and FCMIDLE1 and FCRING1 and FCPINKY1:
            Pose[1] = "Point"
        elif FCINDEX1 and FCMIDLE1 and FCRING1 and FCPINKY1:
            Pose[1] = "Fist"
        if (not FCINDEX2) and FCMIDLE2 and FCRING2 and FCPINKY2:
            Pose[0] = "Point"
        elif FCINDEX2 and FCMIDLE2 and FCRING2 and FCPINKY2:
            Pose[0] = "Fist"
        if Pose[0] == "Point" and Pose[1] == "Fist":
            print("TAP!")
            winList = get_window_info()
            PossibleList = []
            objN.moveTo(int(INDEXX2*Xresolution), int(INDEXY2*Yresolution))
            for win in winList:
                if win[2][0]<INDEXX2*Xresolution and INDEXX2*Xresolution<win[2][0]+win[3][0] and win[2][1]<INDEXY2*Yresolution and INDEXY2*Yresolution<win[2][1]+win[3][1]:
                    PossibleList.append(win)
            print(win[0][0])
            if win[0][0] != objN.title:
                objN = gw.getWindowsWithTitle(win[0][0])[-1]
                objN.restore()
            print(f"Position2 : {[INDEXX2, INDEXY2]}")
        elif Pose[0] == "Fist" and Pose[1] == "Point":
            print("TAP!")
            winList = get_window_info()
            PossibleList = []
            if objN != None:
                objN.moveTo(int(INDEXX1*Xresolution), int(INDEXY1*Yresolution))
            for win in winList:
                if win[2][0]<INDEXX1*Xresolution and INDEXX1*Xresolution<win[2][0]+win[3][0] and win[2][1]<INDEXY1*Yresolution and INDEXY1*Yresolution<win[2][1]+win[3][1]:
                    PossibleList.append(win)
            print(win[0][0])
            if win[0][0] != objN.title:
                objN = gw.getWindowsWithTitle(win[0][0])[-1]
                objN.restore()
            print(f"Position2 : {[INDEXX1, INDEXY1]}")
        else:
            print("Untap")
            objN = demo

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)   

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break