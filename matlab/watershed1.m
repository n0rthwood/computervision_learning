clc
tiledlayout(5,3);
rgb = imread('lab_mask1.bmp');
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
nexttile
imshow(Iobrcbr)
title('Opening-Closing by Reconstruction')


fgm = imregionalmax(Iobrcbr);
nexttile
imshow(fgm)
title('Regional Maxima of Opening-Closing by Reconstruction')


I2 = labeloverlay(I,fgm);
nexttile
imshow(I2)
title('Regional Maxima Superimposed on Original Image')

se2 = strel(ones(5,5));
fgm2 = imclose(fgm,se2);
fgm3 = imerode(fgm2,se2);

fgm4 = bwareaopen(fgm3,20);
I3 = labeloverlay(I,fgm4);
nexttile
imshow(I3)
title('Modified Regional Maxima Superimposed on Original Image')

bw = imbinarize(Iobrcbr);
nexttile
imshow(bw)
title('Thresholded Opening-Closing by Reconstruction')

D = bwdist(bw);
DL = watershed(D);
bgm = DL == 0;
nexttile
imshow(bgm)
title('Watershed Ridge Lines')

gmag2 = imimposemin(gmag, bgm | fgm4);

L = watershed(gmag2);

labels = imdilate(L==0,ones(3,3)) + 2*bgm + 3*fgm4;
I4 = labeloverlay(I,labels);
nexttile
imshow(I4)
title('Markers and Object Boundaries Superimposed on Original Image')