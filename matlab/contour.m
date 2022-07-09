clc
he = imread('a.bmp');
%imshow(he), title('H&E image');
text(size(he,2),size(he,1)+15,...
     'lablel', ...
     'FontSize',7,'HorizontalAlignment','right');

lab_he = rgb2lab(he);
ab = lab_he(:,:,2:3);
ab = im2single(ab);
nColors = 3;
% repeat the clustering 3 times to avoid local minima
pixel_labels = imsegkmeans(ab,nColors,'NumAttempts',3);
