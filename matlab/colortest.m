merged_mask=bitor(bitand(BWhsv,BWlab),BWyc);
imshow(merged_mask,[])
morphed=morph2(merged_mask*255)
%imshow(morphed,[])