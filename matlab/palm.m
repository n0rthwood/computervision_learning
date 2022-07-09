
rgb = imread('a.bmp');
I = rgb2gray(rgb);

nexttile
imshow(I)

text(732,501,'Image courtesy of Corel(R)',...
     'FontSize',7,'HorizontalAlignment','right')


gmag = imgradient(I);
nexttile
imshow(gmag,[])
title('Gradient Magnitude')


L = watershed(gmag);
Lrgb = label2rgb(L);
nexttile
imshow(Lrgb)
title('Watershed Transform of Gradient Magnitude')

se = strel('disk',20);
Io = imopen(I,se);
nexttile
imshow(Io)
title('Opening')

Ie = imerode(I,se);
Iobr = imreconstruct(Ie,I);
nexttile
imshow(Iobr)
title('Opening-by-Reconstruction')
%waitforbuttonpress

IobrGray=im2gray(Iobr)
nexttile
imshow(IobrGray)

title('Opening-by-Reconstruction Gray')
%waitforbuttonpress

Ioc = imclose(Io,se);
nexttile
imshow(Ioc)
title('Opening-Closing')



Iobrd = imdilate(Iobr,se);
Iobrcbr = imreconstruct(imcomplement(Iobrd),imcomplement(Iobr));
Iobrcbr = imcomplement(Iobrcbr);


lab_he = Iobrcbr
ab = lab_he(:,:,1   :1);
ab = im2single(ab);
nColors = 3;
% repeat the clustering 3 times to avoid local minima
pixel_labels = imsegkmeans(ab,nColors,'NumAttempts',3);

mask1 = pixel_labels==1;
cluster1 = he .* uint8(mask1);

X= rgb2gray(cluster1)
BW = false(size(X,1),size(X,2));

% 泛洪填充
row = 101;
column = 189;
tolerance = 12;
addedRegion = grayconnected(X, row, column, tolerance);
BW = BW | addedRegion;

% 使用 diamond 执行掩膜开运算
radius = 20;
se = strel('diamond', radius);
BW = imopen(BW, se);

% Create masked image.
maskedImage = X;
maskedImage(~BW) = 0;

imshow(maskedImage)