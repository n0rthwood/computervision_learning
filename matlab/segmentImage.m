function [mask] = segmentImage(oI)
    
    ycbcrMk=yCbCrMask(oI)
    hsvMK=hsvMask(oI)
    rgbMK=rgbMask(oI)
    ychsFuse=imfuse(ycbcrMk,hsvMK,"blend")
    fullFuse=imfuse(ychsFuse,rgbMK,"blend")
    mask=morph2(fullFuse)
end

