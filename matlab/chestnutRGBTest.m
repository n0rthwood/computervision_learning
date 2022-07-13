oI=imread("../testbmp/cc11.bmp")
mk=CHESTNUTRGBMask(oI)
mkI=im2uint8(mk)
imshowpair(oI,mk,"blend")
