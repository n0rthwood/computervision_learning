import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.segmentation import watershed


# print('temp_path: '+config.temp_path)
# for watershed , check http://bebi103.caltech.edu.s3-website-us-east-1.amazonaws.com/2015/tutorials/r8_watershed_transform.html very good tutorial
def check_double_skiimage(image, debug=False):
    # image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    oI = image.copy()
    kernel = np.ones((10, 10), np.uint8)
    image = cv.morphologyEx(image, cv.MORPH_OPEN, kernel,
                            iterations=4)  # this is to remove noise on the border of the image when object crossed the board left with a small part.

    distance_kernel = np.ones((20, 20), np.uint8)
    distance = ndi.distance_transform_edt(image)
    # footprint and min_distance are important parameters for watershed. min_distance is set to the smallest date width. if object smaller than this, double won't be reliable. abc
    coords = peak_local_max(distance, footprint=np.ones((10, 90)), min_distance=70, labels=image)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)

    labels = watershed(-distance, markers, mask=image)
    count = len(np.unique(labels)) - 1

    # if debug:
    fig = draw_double_skiimage(oI, image, distance, markers, labels, count)
    if not debug:
        plt.close(fig)
    return count, fig


def draw_double_skiimage(oI, image, distance, markers, labels, count):
    fig, axes = plt.subplots(ncols=5, figsize=(9, 3), sharex=True, sharey=True)
    ax = axes.ravel()
    ax[0].imshow(oI, cmap=plt.cm.gray)
    ax[0].set_title('Original')
    ax[1].imshow(image, cmap=plt.cm.gray)
    ax[1].set_title('Overlapping objects')
    ax[2].imshow(-distance, cmap=plt.cm.gray)
    ax[2].set_title('Distances')
    ax[3].imshow(markers, cmap=plt.cm.viridis)
    ax[3].set_title('Peak local max')
    ax[4].imshow(labels, cmap=plt.cm.gray)
    ax[4].set_title('Separated objects' + str(count))
    for a in ax:
        a.set_axis_off()
    fig.tight_layout()
    return fig
    # plt.close(fig)


def check_double(img_mask, debug=False):
    img_mask_3channel = cv.cvtColor(img_mask, cv.COLOR_GRAY2RGB)
    gray = img_mask
    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    thresh = cv.bitwise_not(thresh)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=3)

    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.8 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    unknown_area = cv.subtract(sure_bg, sure_fg)
    # Finding unknown region

    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown_area == 255] = 0

    markers = cv.watershed(img_mask_3channel, markers)
    ws = len(np.unique(markers)) - 1

    surface = np.uint8(sure_fg.copy() * 255)

    contours_wd, _ = cv.findContours(surface, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for ii in range(len(contours_wd)):
        cv.drawContours(surface, contours_wd, ii, (ii + 1), -1)

    count = len(contours_wd)
    fig = None
    if debug:
        fig = draw_double_debug(img_mask, count, thresh, opening, sure_bg, dist_transform, sure_fg, unknown_area,
                                markers)
    return count, thresh, opening, sure_bg, dist_transform, sure_fg, unknown_area, markers, fig


def draw_double_debug(img_mask, count, thresh, opening, sure_bg, dist_transform, sure_fg, unknown_area, markers):
    h, w, ccoo = img_mask.shape
    cv.putText(img_mask, 'count:' + str(count), (2, h - 7), cv.FONT_HERSHEY_SIMPLEX,
               0.7, (0, 0, 255), 1, cv.LINE_AA)

    img_mask[markers == -1] = [0, 0, 255]
    f, ax = plt.subplots(2, 5, figsize=(20, 10))
    axarr = ax.flat
    axarr[0].imshow(thresh, cmap='gray')
    axarr[0].set_title('thresh')  # get the title property handler
    axarr[0].axis('off')
    axarr[1].imshow(opening, cmap='gray')
    axarr[1].set_title('opening')  # get the title property handler
    axarr[1].axis('off')
    axarr[2].imshow(sure_bg, cmap='gray')
    axarr[2].set_title('sure_bg')  # get the title property handler
    axarr[2].axis('off')
    axarr[3].imshow(dist_transform, cmap='gray')
    axarr[3].set_title('dist_transform')  # get the title property handler
    axarr[3].axis('off')
    axarr[4].imshow(sure_fg, cmap='gray')
    axarr[4].set_title('sure_fg')  # get the title property handler
    axarr[4].axis('off')
    axarr[5].imshow(unknown_area, cmap='gray')
    axarr[5].set_title('unknown')  # get the title property handler
    axarr[5].axis('off')
    axarr[6].imshow(markers, cmap='gray')
    axarr[6].set_title('markers')  # get the title property handler
    axarr[6].axis('off')
    axarr[7].imshow(cv.cvtColor(img_mask, cv.COLOR_BGR2RGB))
    axarr[7].set_title('img')  # get the title property handler
    axarr[7].axis('off')
    return f
