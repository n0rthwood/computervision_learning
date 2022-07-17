import cv2
from joycv.features.double import check_double

def find_contours(sliced_mask):
    contours, hierarchy = cv2.findContours(sliced_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_existance(contours):
    if  len(contours) > 0:
        return 1
    else:
        return 0

def find_size(contours):
    contour_max = max(contours, key=cv2.contourArea, default=0)
    left = tuple(contour_max[contour_max[:, :, 0].argmin()][0])
    right = tuple(contour_max[contour_max[:, :, 0].argmax()][0])
    top = tuple(contour_max[contour_max[:, :, 1].argmin()][0])
    bottom = tuple(contour_max[contour_max[:, :, 1].argmax()][0])

    width = right[0]-left[0];
    height = bottom[1]-top[1];
    rect = (left[0],top[1]), (right[0],bottom[1])
    return width, height, rect,contour_max,left,right,top,bottom

def find_color(sliced_image,sliced_mask):
    YCrCb_mean = cv2.mean(cv2.cvtColor(sliced_image, cv2.COLOR_RGB2YCrCb), sliced_mask)
    return YCrCb_mean

def find_double(img_mask):
    count,thresh,opening,sure_bg,dist_transform,sure_fg,unknown_area,markers = check_double(img_mask)
    return count

def draw_debug_info(sliced_img,contour_max,left,right,top,bottom,width,height,YCrCb_mean,double_count):
    cv2.drawContours(sliced_img, [contour_max], -1, (36, 255, 12), 2)
    cv2.circle(sliced_img, left, 8, (0, 50, 255), -1)
    cv2.circle(sliced_img, right, 8, (0, 255, 255), -1)
    cv2.circle(sliced_img, top, 8, (255, 50, 0), -1)
    cv2.circle(sliced_img, bottom, 8, (255, 255, 0), -1)
    h, w, ccoo = sliced_img.shape
    cv2.rectangle(sliced_img, (left[0], top[1]), (right[0], bottom[1]), (255, 0, 0), 2)
    label = 'w:' + str(width) \
            + ' h:' + str(height) \
            + ' c:' + str(round(YCrCb_mean[0])) \
            + ' d:' + str(double_count)

    cv2.putText(sliced_img, label, (2, h - 5), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0), 1, cv2.LINE_AA)