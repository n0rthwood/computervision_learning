import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import cv2
from skimage.segmentation import watershed
from skimage.feature import peak_local_max

image = np.load('/var/folders/jd/lb66sbsn2zqdtfrp2ng2xkn80000gn/T/joycv_tmp/fd1_sliced_mask_1_2.npy')
# Now we want to separate the two objects in image
# Generate the markers as local maxima of the distance to the background
distance = ndi.distance_transform_edt(image)
coords = peak_local_max(distance, footprint=np.ones((50, 50)), labels=image)
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