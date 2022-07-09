clc;clear
fixed = imread('a.bmp');
moving = imread('bg.bmp');

%imshowpair(fixed, moving,'blend')
[optimizer, metric] = imregconfig('multimodal')
% 
% optimizer.InitialRadius = 0.009;
% optimizer.Epsilon = 1.5e-4;
% optimizer.GrowthFactor = 1.01;
% optimizer.MaximumIterations = 300;

grey1=rgb2gray(moving)
grey2=rgb2gray(fixed)
movingRegistered = imregister(grey1, grey2, 'affine', optimizer, metric);
figure
imshowpair(fixed, movingRegistered,'falsecolor')