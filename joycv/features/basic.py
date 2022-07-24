import cv2

from .double import check_double, check_double_skiimage


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

def extract_basic_feature(contour_rect_and_contour_for_each_grid,image,sliced_training_size=224,padding=3):
    basic_info = []

    contour_rects=contour_rect_and_contour_for_each_grid[0]
    contours=contour_rect_and_contour_for_each_grid[1]
    masks = contour_rect_and_contour_for_each_grid[2]
    for image_index in range(len(contour_rects)):
        if(len(contour_rects[image_index])>0):
            contour_rect=contour_rects[image_index]
            contour=contours[image_index]
            mask = masks[image_index]
            double_count = find_double(mask)
            #unpack y,x,h,w from contour_rect
            x,y,w,h = contour_rect

            centerw = x+w/2
            centereh = y+h/2

            cutx = round(centerw-sliced_training_size/2)
            cuty = round(centereh-sliced_training_size/2)
            if cutx<0:cutx=0
            if cuty<0:cuty=0
            if cutx+w>image.shape[1]:cutx=image.shape[1]-sliced_training_size
            if cuty+h>image.shape[0]:cuty=image.shape[0]-sliced_training_size

            cut_rect = (cutx,cuty,224,224)
            #slice the image
            sliced_image = image[y:y+h, x:x+w]

            color = round(find_color(sliced_image, mask))

            #unpack the rect to x,y,w,h
            x,y,w,h = contour_rect
            x=x-padding
            y=y-padding
            w=w+padding*2
            h=h+padding*2
            if x<0:x=0
            if y<0:y=0
            if x+w>image.shape[1]:w=image.shape[1]-x
            if y+h>image.shape[0]:h=image.shape[0]-y
            save_rect=(x,y,w,h)
            rect = contour_rect
            exist = 1;
            basic_info.append([exist,double_count,color,rect,cut_rect])

        else:

            basic_info.append([])


    return basic_info

def draw_debug_rect_on_each_object_on_whole_image(contour_rect_for_each_grid,orig_image,basic_info,rows,columns):
    whole_image=orig_image.copy()
    contour_rect=contour_rect_for_each_grid[0]
    contour=contour_rect_for_each_grid[1]
    mask = contour_rect_for_each_grid[2]
    for image_index in range(len(basic_info)):
        if(len(basic_info[image_index])>0):

            color = basic_info[image_index][2]
            double_count = basic_info[image_index][1]
            exist = basic_info[image_index][0]
            rect =  basic_info[image_index][3]
            cut_rect = basic_info[image_index][4]

            row_index=round(image_index//columns)
            column_index=round(image_index%columns)
            cv2.rectangle(whole_image, rect, (0, 255, 0), 2)
            if double_count<2 : cv2.rectangle(whole_image, cut_rect, (0, 0, 255), 1)
            cv2.drawContours(whole_image, contour[image_index], -1, (0, 0, 255), 2)
            cv2.putText(whole_image, "row: " + str(row_index) + ",col: " + str(column_index) + " e:" + str(exist) , (rect[0], rect[1]  -  18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(whole_image, "w:" + str(rect[2]) + " h:" + str(rect[3]) + " c:" + str(round(color)), (rect[0],  rect[1] + rect[3]  + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(whole_image, "d:" + str(double_count) + ",area: " + str(rect[2] * rect[3]), (rect[0], rect[1] + rect[3]  + 43), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    return whole_image
def slice_image_according_to_rect(image, rects):

    sliced_images = []
    for rect in rects:
        x, y, w, h = rect
        sliced_image = image[y:y+h, x:x+w]
        sliced_images.append(sliced_image)
    return sliced_images

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
    YCrCb_mean = cv2.mean(cv2.cvtColor(sliced_image, cv2.COLOR_RGB2YCrCb), sliced_mask)[0]
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

def for_each_mask_find_countour_rect(single_restored_sized_mask, columns=6, rows=4):
    contours = find_contours(single_restored_sized_mask)
    contours_rects = [cv2.boundingRect(contour) for contour in contours]
    #extract h and w from overall_mask
    h, w = single_restored_sized_mask.shape
    grid_h = h // rows
    grid_w = w // columns
    #extract each grid rect  from single_restored_sized_mask
    grid_rects = [ (grid_w * j, grid_h * i,grid_w, grid_h)  for i in range(rows)  for j in range(columns)]

    contour_rect_for_each_grid = [];
    contour_for_each_grid = [];
    mask_for_each_grid = [];

    for grid_rect_index in range(len(grid_rects)) :
        for contour_rec_index in range (len(contours_rects)):
            if overlap_region_percentage(contours_rects[contour_rec_index],grid_rects[grid_rect_index])>0.5 and contours_rects[contour_rec_index][2]*contours_rects[contour_rec_index][3]>5000 and  contours_rects[contour_rec_index][2]>70 and contours_rects[contour_rec_index][3]>70:
                contour_rect_for_each_grid.append(contours_rects[contour_rec_index])
                contour_for_each_grid.append(contours[contour_rec_index])
                mask_for_each_grid.append(single_restored_sized_mask[contours_rects[contour_rec_index][1]:contours_rects[contour_rec_index][1]+contours_rects[contour_rec_index][3],contours_rects[contour_rec_index][0]:contours_rects[contour_rec_index][0]+contours_rects[contour_rec_index][2]])
                break
            else:
                continue
        if(len(contour_rect_for_each_grid)-1!=grid_rect_index):
            contour_rect_for_each_grid.append(())
            contour_for_each_grid.append(())
            mask_for_each_grid.append(())


    return [contour_rect_for_each_grid,contour_for_each_grid,mask_for_each_grid]
