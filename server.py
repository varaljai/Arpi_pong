import cv2
import socket
import mediapipe as mp
import time




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),5055))
s.listen(2)
clientsocket, adress = s.accept()


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils



while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                
                if id == 8:
                    print(id, cx, cy)
                    cv2.circle(img, (cx, cy), 10, (255, 255, 0), cv2.FILLED)
                    adat = (id,cx,cy)
                    

                    
                    if clientsocket:
                        clientsocket.send(bytes(str(adat),'utf-8'))

    cv2.imshow('image', img)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()