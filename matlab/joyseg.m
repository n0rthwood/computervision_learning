function joyseg(oI)
ycbcrMk=yCbCrMask(oI);
hsvMK=hsvMask(oI);
rgbMK=rgbMask(oI);
labMK=labMask(oI);
ychsFuse=imfuse(ycbcrMk,hsvMK,"blend");
fullFuse=imfuse(ychsFuse,labMK,"blend");
final=morph2(fullFuse);
Filename = sprintf('tmp/%s.bmp', datestr(now,'mm-dd-yyyy HH-MM-SS'));
imwrite(imfuse(oI,final,"blend"),Filename);
end