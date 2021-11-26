# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import pyautogui
from datetime import datetime
import math
#import webbrowser

kkkk = False

def win():
    if kkkk == False:
        #webbrowser.open('https://en.wikipedia.org/wiki/List_of_sexually_active_popes')
        pyautogui.press('space')
        pyautogui.keyDown('win')
        pyautogui.press('d')
        pyautogui.keyUp('win')
        pyautogui.press('volumemute')


aaa = str(input('Deseja ajustar a câmera antes de iniciar o programa? Digite "s" ou "n".\n')).strip().lower()

if aaa[0:1] == 's':
    kkkk = True
else:
    print('Carregando...')
    time.sleep(5)

hora1 = int(str(datetime.now())[17:19])

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start() # <------------------------------------- Src 0,1,2,3,4.... = webcam usada
    time.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None
a = 'a'

h1 = 0

# loop over the frames of the video
while True:
    time.sleep(0.05)
    horaatual = int(str(datetime.now())[17:19])
    if horaatual - hora1 > 10:  # <------------------------------------------ 10 m: A cada 10 segundos a imagem de referência reinicia
        firstFrame = None
        hora1 = int(str(datetime.now())[17:19])
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()[300:480, 195:640]  # <--------------------------------------- AJUSTE AQUI O CORTE DO VIDEO
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        now1 = datetime.now()
        noww = int(str(now1)[17:19])
        #print(noww)
        ragatanga = str(datetime.now())[14:16]

        if str(now1)[14:16] != ragatanga or int(math.sqrt(((noww) - int(h1)) ** 2)) >= 20:  # <------------------------- 20s = cooldown para novo disparo
            win()
            now = datetime.now()
            # print(int(h1))
            # print(int(noww))
            h1 = str(now)[17:19]
            ragatanga = str(now)[14:16]
            print('Movimento detectado!\n' + str(now))

    # draw the text and timestamp on the frame
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    # cv2.imshow("Thresh", thresh)
    # cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
