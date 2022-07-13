% function color_merge()
i=imread("../../testbmp/cc7.bmp");
hsvMK=hsv(i);
ycbcrMK=ycbcr(i);
labMK=lab(i);

step1=bitor(hsvMK,ycbcrMK);
step2=bitor(step1,labMK);

mask_merged=uint8(imcomplement(step2)*255);
mask_merged=morphcloseopen(mask_merged);
nexttile
imshow(mask_merged)
title("fullFused")

nexttile
imshowpair(i,mask_merged,"blend")
title("blend")

nexttile
imshow(hsvMK);
title("hsvMK")

nexttile
imshow(ycbcrMK);
title("ycbcrMK")

nexttile
imshow(labMK);
title("labMK")
% end