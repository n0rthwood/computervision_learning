import cv2


def close_and_open(mask, close_kernel_size=5, open_kernel_size=28):
    mmorphed_kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_kernel_size, close_kernel_size))
    mmorphed_mk = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, mmorphed_kernal, iterations=2)

    mmorphed_kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_kernel_size, open_kernel_size))
    mmorphed_mk = cv2.morphologyEx(mmorphed_mk, cv2.MORPH_OPEN, mmorphed_kernal, iterations=2)
    return mmorphed_mk

def open_and_close(mask, open_kernel_size=5, close_kernel_size=28):
    mmorphed_kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_kernel_size, open_kernel_size))
    mmorphed_mk = cv2.morphologyEx(mask, cv2.MORPH_OPEN, mmorphed_kernal, iterations=2)

    mmorphed_kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_kernel_size, close_kernel_size))
    mmorphed_mk = cv2.morphologyEx(mmorphed_mk, cv2.MORPH_CLOSE, mmorphed_kernal, iterations=2)
    return mmorphed_mk