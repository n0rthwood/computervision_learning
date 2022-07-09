clear
close all

I=imread("a.bmp")
I1=rgb2gray(I)
%imshow(I)

background=imread("bg.bmp")
%imshow(background)
b1=rgb2gray(background)

tformEstimate = imregcorr(I,background);
Rfixed = imref2d(size(background));

movingReg = imwarp(I,tformEstimate,'OutputView',Rfixed);

%I2=imsubtract(I1,b1)
I2=imabsdiff(I,movingReg)
figure,imshow(I2)
waitforbuttonpress