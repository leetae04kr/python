import numpy as np
import cv2
from collections import deque

# "파란색"으로 간주 할 색상의 상한 및 하한을 정의합니다.
blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

# 침식 및 팽창을위한 5x5 커널 정의
kernel = np.ones((5, 5), np.uint8)

# 별도의 배열에 별도의 색상을 저장하는 데크 설정
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]

bindex = 0
gindex = 0
rindex = 0
yindex = 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# 그림판 인터페이스 설정
paintWindow = np.zeros((471,636,3)) + 255
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), colors[3], -1)
cv2.putText(paintWindow, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

#비디오로드
camera = cv2.VideoCapture(0)
#jupyter noteboook 에서 여기까지 실행하고, print(camera.read()) 해서 프레임을 살펴보고, 프레임을 늘리는 방법을 알아보

# 계속 반복
while True:
    # 현재 paintWindow 잡기
    (grabbed, frame) = camera.read()
    ##디버깅 작업 한번하기
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 프레임에 색상 옵션 추가
    frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv2.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv2.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv2.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv2.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    # 비디오의 끝에 도달했는지 확인하십시오.
    if not grabbed:
        break

    # 파란색 경계에 속하는 픽셀을 확인한 다음 이진 이미지를 흐리게합니다.
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # 이미지에서 윤곽선 찾기
    (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # 윤곽선이 발견되었는지 확인하십시오.
    if len(cnts) > 0:
    	# 윤곽선을 정렬하고 가장 큰 윤곽선을 찾습니다.
    	# 이 윤곽선이 마커 캡의 영역과 일치한다고 가정합니다.
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        #발견 된 윤곽선 주위를 둘러싼 원의 반경을 가져옵니다.
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # 윤곽선 주위에 원을 그립니다.
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # 윤곽의 중심 (이 경우 원)을 계산할 모멘트를 얻습니다.
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        if center[1] <= 65:
            if 40 <= center[0] <= 140: # 모두 지우기
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                bindex = 0
                gindex = 0
                rindex = 0
                yindex = 0

                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # 파랑
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # 초록
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # 빨강
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # 노랑
        else :
            if colorIndex == 0:
                bpoints[bindex].appendleft(center)
            elif colorIndex == 1:
                gpoints[gindex].appendleft(center)
            elif colorIndex == 2:
                rpoints[rindex].appendleft(center)
            elif colorIndex == 3:
                ypoints[yindex].appendleft(center)
    # 윤곽선이 감지되지 않은 경우 다음 데크를 추가합니다 (예 : 마커 캡 반전).
    else:
        bpoints.append(deque(maxlen=512))
        bindex += 1
        gpoints.append(deque(maxlen=512))
        gindex += 1
        rpoints.append(deque(maxlen=512))
        rindex += 1
        ypoints.append(deque(maxlen=512))
        yindex += 1

    # 모든 색상 (파란색, 녹색, 빨간색 및 노란색)의 선을 그립니다.
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    # 프레임 및 paintWindow 이미지 표시
    cv2.imshow("Tracking(maid by lty)", frame)
    cv2.imshow("Paint(maid by lty)", paintWindow)

	# 'z'키를 누르면 루프 중지
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 카메라를 정리하고 열려있는 모든 창을 닫습니다.
camera.release()
cv2.destroyAllWindows()


    
