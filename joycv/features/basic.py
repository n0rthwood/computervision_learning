import cv2

from features.double import check_double, check_double_skiimage


def find_contours(sliced_mask):
    contours, hierarchy = cv2.findContours(sliced_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_existance(contours):
    if len(contours) > 0:
        return 1
    else:
        return 0

#找到每个扣出来的物体的轮廓
def find_mask_boundary(contour):
    left = tuple(contour[contour[:, :, 0].argmin()][0])
    right = tuple(contour[contour[:, :, 0].argmax()][0])
    top = tuple(contour[contour[:, :, 1].argmin()][0])
    bottom = tuple(contour[contour[:, :, 1].argmax()][0])

    rect = (left[0], top[1]), (right[0], bottom[1])
    return  rect

#计算每个扣出物体在网格4*6（或者其他尺寸）中的面积占比。后期需要对比占比是否大于50%来确定是否属于这个网格
def overlap_region_percentage(mask_rec, grid_rec):
    x1,y1,w1,h1 = mask_rec
    x2,y2,w2,h2 = grid_rec
    x_overlap = max(0, min(x1+w1,x2+w2)-max(x1,x2))
    y_overlap = max(0, min(y1+h1,y2+h2)-max(y1,y2))
    overlap_area = x_overlap * y_overlap
    total_area = w1 * h1
    return overlap_area/total_area

def find_size(contours):
    contour_max = max(contours, key=cv2.contourArea, default=0)
    left = tuple(contour_max[contour_max[:, :, 0].argmin()][0])
    right = tuple(contour_max[contour_max[:, :, 0].argmax()][0])
    top = tuple(contour_max[contour_max[:, :, 1].argmin()][0])
    bottom = tuple(contour_max[contour_max[:, :, 1].argmax()][0])

    width = right[0] - left[0];
    height = bottom[1] - top[1];
    rect = (left[0], top[1]), (right[0], bottom[1])
    return width, height, rect, contour_max, left, right, top, bottom


def find_color(sliced_image, sliced_mask):
    YCrCb_mean = cv2.mean(cv2.cvtColor(sliced_image, cv2.COLOR_RGB2YCrCb), sliced_mask)
    return YCrCb_mean


def find_double(img_mask):
    count, thresh, opening, sure_bg, dist_transform, sure_fg, unknown_area, markers = check_double(img_mask)
    return count


def find_double_skiimage(image, draw_debug=False):
    count, subfig = check_double_skiimage(image, draw_debug)
    return count, subfig


def draw_debug_info(sliced_img, contour_max, left, right, top, bottom, width, height, YCrCb_mean, double_count,
                    draw_debug=False):
    debug_label = 'w:' + str(width) \
                  + ' h:' + str(height) \
                  + ' c:' + str(round(YCrCb_mean[0])) \
                  + ' d:' + str(double_count)

    cv2.drawContours(sliced_img, [contour_max], -1, (36, 255, 12), 2)
    cv2.circle(sliced_img, left, 8, (0, 50, 255), -1)
    cv2.circle(sliced_img, right, 8, (0, 255, 255), -1)
    cv2.circle(sliced_img, top, 8, (255, 50, 0), -1)
    cv2.circle(sliced_img, bottom, 8, (255, 255, 0), -1)
    h, w, ccoo = sliced_img.shape
    cv2.rectangle(sliced_img, (left[0], top[1]), (right[0], bottom[1]), (255, 0, 0), 2)
    # cv2.putText(sliced_img, debug_label, (2, h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    return debug_label


def extract_img(image, mask):
    img_mask = cv2.bitwise_and(image, image, mask=mask)
    return img_mask
