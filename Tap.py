import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

cap = cv2.VideoCapture(0)  # Use 0 for webcam

pendLimitI = -10
pendLimitM = -10
pendLimitR = -10
pendLimitP = -10
pending = False
pender = 0
lastPendTime = time.time() # time in seconds

while cap.isOpened():
    if time.time() - lastPendTime > 1:
        print(f"Pending time: {time.time() - lastPendTime}")
        print(f"Pending count: {pender}")
        lastPendTime = time.time()
        pender = 0
    if pender > 1:
        print("TAP!")
        pender = 0
    success, image = cap.read()
    if not success:
        print("Failed to read image.")
        break
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hand.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        Landmarks = results.multi_hand_landmarks[-1]
        Names = ["WRIST", "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP", "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP", "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP", "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP", "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"]
        #for i in range(21):
        #    print(i, Names[i], Landmarks.landmark[i])
        WRISTX = Landmarks.landmark[0].x
        WRISTY = Landmarks.landmark[0].y
        WRISTZ = Landmarks.landmark[0].z
        THUMBX = Landmarks.landmark[4].x
        THUMBY = Landmarks.landmark[4].y
        THUMBZ = Landmarks.landmark[4].z
        INDEXX = Landmarks.landmark[8].x
        INDEXY = Landmarks.landmark[8].y
        INDEXZ = Landmarks.landmark[8].z
        MIDDLEX = Landmarks.landmark[12].x
        MIDDLEY = Landmarks.landmark[12].y
        MIDDLEZ = Landmarks.landmark[12].z
        RINGX = Landmarks.landmark[16].x
        RINGY = Landmarks.landmark[16].y
        RINGZ = Landmarks.landmark[16].z
        PINKYX = Landmarks.landmark[20].x
        PINKYY = Landmarks.landmark[20].y
        PINKYZ = Landmarks.landmark[20].z

        sqrt = lambda x: x**0.5

        WTD = sqrt((WRISTX - THUMBX)**2 + (WRISTY - THUMBY)**2 + (WRISTZ - THUMBZ)**2)
        WID = sqrt((WRISTX - INDEXX)**2 + (WRISTY - INDEXY)**2 + (WRISTZ - INDEXZ)**2)
        WMD = sqrt((WRISTX - MIDDLEX)**2 + (WRISTY - MIDDLEY)**2 + (WRISTZ - MIDDLEZ)**2)
        WRD = sqrt((WRISTX - RINGX)**2 + (WRISTY - RINGY)**2 + (WRISTZ - RINGZ)**2)
        WPD = sqrt((WRISTX - PINKYX)**2 + (WRISTY - PINKYY)**2 + (WRISTZ - PINKYZ)**2)
        # print(f"Distance between WRIST and THUMB : {WTD}")
        # print(f"Distance between WRIST and INDEX : {WID}")
        # print(f"Distance between WRIST and MIDLE : {WMD}")
        # print(f"Distance between WRIST and RIING : {WRD}")
        # print(f"Distance between WRIST and PINKY : {WPD}")
        # print()

        LIMITPOINT = 0.34
        if WID > LIMITPOINT and WMD > LIMITPOINT and WRD > LIMITPOINT and WPD > LIMITPOINT:
            print("Pointing!")
            pending = True
            pendLimitI = max(WID/2.1, LIMITPOINT)
            pendLimitM = max(WMD/2.1, LIMITPOINT)
            pendLimitR = max(WRD/2.1, LIMITPOINT)
            pendLimitP = max(WPD/2.1, LIMITPOINT)
        elif WID < pendLimitI and WMD < pendLimitM and WRD < pendLimitR and WPD < pendLimitP and pending:
            print("Pending!")
            pending = False
            lastPendTime = time.time()
            pender += 1

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(10) & 0xFF == 27:
        break