  
import cv2
import numpy as np


def get_contours( image ):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)            # detects points with color change
    x = y = w = h = 0                                                                                # if area less than 200, returned value should not be None
    for contour in contours:
        area = cv2.contourArea(contour)                                                              # detects portion with a particular contour

        if area > 200:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            x, y, w, h = cv2.boundingRect(approx)                                                    # returns diagonal points of the rectangule drawn

    return x + w // 2, y + w // 2


def draw_on_canvas(points, BGR_values):
    for point in points:
        cv2.circle(final_result, (point[0], point[1]), 10, BGR_values[point[2]], cv2.FILLED)               # fills the particular point with it's respective color


def find_color(image, my_colors, BGR_values):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                           # to convert Image into HSV

    for i, color in enumerate(my_colors):
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(img_hsv, lower, upper)                            # masks for all points of one color
        x, y = get_contours(mask)

        if x != 0 and y != 0:                                                # attaches point to the list only if it is not at origin
            points.append((x, y, i))

        draw_on_canvas(points, BGR_values)

width ,height=2500,1500

# my_colors include HSV ranges and BGR_values include BGR ranges of the respective colors
my_colors = [[0, 0, 0, 180, 255, 30],                  # black
             [138, 22, 85, 179, 127, 255],             # pink
             [94, 80, 2, 126, 255, 255],               # blue
             [20, 100, 100, 30, 255, 255],             # yellow
             [57, 76, 0, 100, 255, 255],               # green
             [0, 50, 50, 10, 255, 255]]                # red

points = []

BGR_values = [[0, 0, 0],
              [255, 51, 255],
              [255, 0, 0],
              [0, 255, 255],
              [0, 255, 0],
              [0, 0, 255]]

captured = cv2.VideoCapture(0)
captured.set(3, width)  # width
captured.set(4, height)  # height
captured.set(10, 130)

while True:
    success , image = captured .read()
    if not success:
        print("Camera not accessed , please check the issue")
        break

    final_result = image.copy()
    find_color(image, my_colors, BGR_values)                                  # to detect colors

    cv2.imshow('final', final_result)

    if cv2.waitKey(1) & 0XFF == ord('q'):                                   # press 'q' to exit
        cv2.destroyAllWindows()
        break
