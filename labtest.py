#load image a.bmp and convert it to lab color space (L*a*b) then convert it to single prcesition floating point without lightness channel  show the result image alongside the original
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

image = cv2.imread('matlab/cc.bmp')

plt.figure()
# plt.imshow(image)
# plt.show()
imageLab = cv2.cvtColor(image, cv2.COLOR_RGB2Lab)
imageLab = image[:,:,1:2]
#
plt.imshow(imageLab)
plt.show()
#kmeans clustering 2 clusters
kmeans = KMeans(init='k-means++', n_clusters=3, n_init=10)
fitImageLab=imageLab.reshape(-1, 1)
kmeans.fit(fitImageLab)
P = kmeans.predict(fitImageLab)
P = P.reshape(imageLab.shape)
plt.figure()
plt.imshow(P, cmap='gray')
plt.show()


exit()