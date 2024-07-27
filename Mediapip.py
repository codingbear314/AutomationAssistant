import mediapipe as mp
import cv2
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)  # Use 0 for webcam

while cap.isOpened():
    success, image = cap.read()
    print(type(image))
    if not success:
        break

    # Convert the BGR image to RGB, flip the image around y-axis for correct handedness output
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image and draw hand landmarks
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        print(results.multi_hand_landmarks)
        print(type(results.multi_hand_landmarks))
        print(len(results.multi_hand_landmarks[0]))
        print(type(results.multi_hand_landmarks[0][0]))
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
    break

time.sleep(10)
cap.release()
cv2.destroyAllWindows()