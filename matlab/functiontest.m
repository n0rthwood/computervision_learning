% I=imread("matlab/cc.bmp")
% ycbcrMK=yCbCrMask(I)
% I1 = I .* uint8(ycbcrMK);
% grayI=rgb2gray(I1)
% mask=morph(grayI)
% imshowpair(I,mask,"blend")
clc;clear
figure
oI=imread("matlab/fullcategory.png");

ycbcrMk=yCbCrMask(oI)
hsvMK=hsvMask(oI)
rgbMK=rgbMask(oI)
labMK=labMask(oI)
nexttile


imshow(ycbcrMk,[])
title("ycbcr")
nexttile


imshow(hsvMK,[])
title("hsvMK")
nexttile


imshow(labMK,[])
title("labMask")
nexttile


imshow(rgbMK,[])
title("rgbMK")
nexttile
ychsFuse=imfuse(ycbcrMk,hsvMK,"blend")
fullFuse=imfuse(ychsFuse,labMK,"blend")
nexttile
imshow(fullFuse)
title("fullFuse")

final=morph2(fullFuse)
imshow(final,[])
title("final")

nexttile
imshowpair(oI,final,"blend")


% labI=rgb2lab(I)
% ab = labI(:,:,2:3);
% ab = im2single(ab);


% pixel_labels = imsegkmeans(ab,4,'NumAttempts',1);
% nexttile()
% title('1')
% imshow(pixel_labels,[])
% 
% 
% I=imread("matlab/b.bmp")
% labI=rgb2lab(I)
% ab = labI(:,:,2:3);
% ab = im2single(ab);
% pixel_labels1 = imsegkmeans(ab,4,'NumAttempts',1);
% nexttile()
% title('2')
% imshow(pixel_labels1,[])
% 
% I=imread("matlab/cc.bmp")
% labI=rgb2lab(I)
% ab = labI(:,:,2:3);
% ab = im2single(ab);
% pixel_labels2 = imsegkmeans(ab,4,'NumAttempts',1);
% nexttile()
% title('3')
% imshow(pixel_labels2,[])
% 
% I=imread("matlab/bg.bmp")
% labI=rgb2lab(I)
% ab = labI(:,:,2:3);
% ab = im2single(ab);
% pixel_labels3 = imsegkmeans(ab,4,'NumAttempts',1);
% nexttile()
% title('4')
% imshow(pixel_labels3,[])
% nexttile
% 
% imshow(pixel_labels,[])
% bw=sitt(pixel_labels)
% nexttile
% imshowpair(I,bw,"blend")