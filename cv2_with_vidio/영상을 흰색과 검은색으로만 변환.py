import cv2
 
capture = cv2.VideoCapture(0)
 
while (True):
 
    (ret, frame) = capture.read()
 
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    (thresh, blackAndWhiteFrame) = cv2.threshold(grayFrame, 127, 255, cv2.THRESH_BINARY)
 
 
    cv2.imshow('video bw', blackAndWhiteFrame)
    cv2.imshow('video original', frame)
 
    if cv2.waitKey(1) == 27:
        break
 
capture.release()
cv2.destroyAllWindows()
