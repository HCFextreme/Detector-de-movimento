# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import pyautogui
from datetime import datetime
import math
import keyboard
#import webbrowser

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

a = 1
kk = 0
while a == 1:
    try:
        video = cv2.VideoCapture(kk, cv2.CAP_DSHOW)
        check, frame = video.read()
        width,height, cu = (frame.shape)
        video.release()
        a = 0
    except:
        kk = kk + 1

kkkk = False

def win():
    if kkkk == False:
        #webbrowser.open('https://en.wikipedia.org/wiki/List_of_sexually_active_popes')
        pyautogui.press('space')
        pyautogui.keyDown('win')
        pyautogui.press('d')
        pyautogui.keyUp('win')
        pyautogui.press('volumemute')
        pyautogui.press('win')


aaa = str(input(bcolors.WARNING + 'Deseja ajustar a câmera antes de iniciar o programa? Digite "s" ou "n" (Aperte ''k'' + ''q'' para encerrar ou reiniciar o teste).\n' + bcolors.ENDC)).strip().lower()

if aaa[0:1] == 's':
    kkkk = True
else:
    print(bcolors.WARNING + 'Carregando...' + bcolors.ENDC)
    time.sleep(5)

hora1 = int(str(datetime.now())[17:19])

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
x = -1
def web():
    global vs
    global x
    x = x+1
    if x == 10:
        x = 0
    if args.get("video", None) is None:
        vs = VideoStream(src=x).start() # <------------------------------------- Src 0,1,2,3,4.... = webcam usada
        time.sleep(2.0)
    # otherwise, we are reading from a video file
    else:
        vs = cv2.VideoCapture(args["video"])

web()

# initialize the first frame in the video stream
firstFrame = None
a1 = 1.6 # <--------------------------------------- AJUSTE AQUI O CORTE DO VIDEO (+a +altura, +b + largura)
b1 = 3.28

h1 = 0

print(bcolors.WARNING + 'Pronto! Aperte as teclas ''q'' + ''z'' para mudar de câmera! (Pode gerar muitos erros que podem ser ignorados!)')

# loop over the frames of the video
while True:
    time.sleep(0.05)
    horaatual = int(str(datetime.now())[17:19])
    if math.sqrt((hora1 - horaatual)**2) > 10:  # <------------------------------------------ 10 m: A cada 10 segundos a imagem de referência reinicia
        firstFrame = None
        hora1 = int(str(datetime.now())[17:19])
    # grab the current frame and initialize the occupied/unoccupied
    # text
    try:
        frame = vs.read()[int(width/a1):width, int(height/b1):height]
    except:
        web()
        continue
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
        noww = int((str(now1)[14:16]) + (str(now1)[17:19]))
        #print(noww)

        if int(math.sqrt(((noww) - h1) ** 2)) >= 20:  # <------------------------- 20s = cooldown para novo disparo
            win()
            now = datetime.now()
            #print(horaatual)
            #print(int(hora1))
            h1 = int((str(now)[14:16]) + (str(now)[17:19]))
            print(bcolors.BOLD + 'Movimento detectado!\n' + str(now) + bcolors.ENDC)


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
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q') and keyboard.is_pressed('z'):  # if key 'q' and 'z' is pressed
            print(bcolors.WARNING + 'Mudando câmera' + bcolors.ENDC)
            time.sleep(0.5)
            web()
            firstFrame = None
        elif keyboard.is_pressed('q') and keyboard.is_pressed('k'):
            if kkkk == True:
                kkkk = False
                time.sleep(0.5)
                print(bcolors.WARNING + "Teste encerrado!" + bcolors.ENDC)
            else:
                kkkk = True
                time.sleep(0.5)
                print(bcolors.WARNING + "Teste iniciado!" + bcolors.ENDC)

    except:
        continue  # if user pressed a key other than the given key the loop will break
# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
