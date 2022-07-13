I=imread("../testbmp/cc7.bmp");
mask=universalRGBMask(I);

I1=imread("../testbmp/fd1.bmp");
mask2=universalRGBMask(I1);

I2=imread("../testbmp/dd3.bmp");
mask3=universalRGBMask(I2);

figure
imshowpair(I,morph2(imcomplement(mask)),"montage")
figure
imshowpair(I1,(imcomplement(mask2)),"montage")
figure
imshowpair(I2,(imcomplement(mask3)),"montage")