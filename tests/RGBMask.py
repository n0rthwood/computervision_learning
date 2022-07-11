import cv2

lower = cv2.legacy.Scalar(0, 0, 0)
upper = cv2.legacy.Scalar(1, 0.225, 1)

image = cv2.imread('matlab/a.bmp')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower, upper)
cv2.imshow('Mask', mask)
