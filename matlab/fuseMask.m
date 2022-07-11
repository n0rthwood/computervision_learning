function [BW] = fuseMask(hsvMK,RGBMK,ycbcrMk)
    ychsFuse=imfuse(ycbcrMk,hsvMK,"blend")
    BW=imfuse(ychsFuse,RGBMK,"blend")
end