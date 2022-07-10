Io = imread("lab_mask1.bmp")
I = im2gray(Io)
BW1 =edge(I,"sobel")
BW2 = edge(I,"canny")


tiledlayout(2,2)

nexttile
imshow(Io)

nexttile
imshow(I)

nexttile
imshow(BW1)
title('Sobel Filter')

nexttile
imshow(BW2)
title('Canny Filter')