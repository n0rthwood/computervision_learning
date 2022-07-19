import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import cv2
from skimage.segmentation import watershed
from skimage.feature import peak_local_max


image = cv2.imread('/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/cc_s1_sliced_image_3_5.png')

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#image = np.load('/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/fd3_sliced_mask_2_1.npy')
# Now we want to separate the two objects in image
# Generate the markers as local maxima of the distance to the background
distance = ndi.distance_transform_edt(image)
coords = peak_local_max(distance, footprint=np.ones((5, 5)), labels=image)
mask = np.zeros(distance.shape, dtype=bool)
mask[tuple(coords.T)] = True
markers, _ = ndi.label(mask)

labels = watershed(-distance, markers, mask=image)
print('no. of object: '+str(  len(np.unique(labels)) - 1))
fig, axes = plt.subplots(ncols=3, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].set_title('Overlapping objects')
ax[1].imshow(-distance, cmap=plt.cm.gray)
ax[1].set_title('Distances')
ax[2].imshow(labels, cmap=plt.cm.gray)
ax[2].set_title('Separated objects')
for a in ax:
    a.set_axis_off()
fig.tight_layout()
plt.show()