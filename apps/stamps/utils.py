import json

import cv2
import numpy as np


def read_image(path):
    # чтение изображения
    im = cv2.imread(path)
    return im


def select_blue_color(im):
    # выбор только синих областей
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    blue_lower = np.array([80, 30, 30])
    blue_higher = np.array([140, 250, 250])
    mask = cv2.inRange(hsv, blue_lower, blue_higher)
    selection = cv2.bitwise_and(im, im, mask=mask)
    return selection, mask


def preprocess_selection(selection):
    # предобработка выбранных областей
    gray = cv2.cvtColor(selection, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    return blur


def find_circles(blur):
    # поиск кругов на изображении
    h, w = blur.shape
    r_min = int(w * 0.15 / 2)
    r_max = int(w * 0.30 / 2)
    contours = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=2 * r_min)
    boxes = []
    if contours is not None:
        for contour in contours[0]:
            xc, yc, r = np.uint16(np.around(contour))
            if r_min <= r <= r_max:
                x1 = xc - r
                y1 = yc - r
                x2 = xc + r
                y2 = yc + r
                boxes.append([x1, y1, x2, y2])
    return boxes


def detect_stamps(image):
    # общая функция для обнаружения печатей на изображении
    im = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    selection, mask = select_blue_color(im)
    blur = preprocess_selection(selection)
    boxes = find_circles(blur)
    if len(boxes) == 0:
        return 0, []
    # im_boxes = annotate_image(im, boxes)
    result = np.array(boxes, dtype=np.uint8)
    return result


def to_json(boxes):
    return json.dumps(boxes, sort_keys=True, indent=4)
