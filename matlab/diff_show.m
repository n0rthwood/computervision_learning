clc

moving = imread("a.bmp");
fixed = imread("bg.bmp");

imshowpair(moving,fixed,"falsecolor")

waitforbuttonpress

figure

tformEstimate = imregcorr(moving,fixed);
Rfixed = imref2d(size(fixed));
movingReg = imwarp(moving,tformEstimate,'OutputView',Rfixed);

imshowpair(fixed,movingReg,'montage')