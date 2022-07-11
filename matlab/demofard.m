srcPath="/Volumes/Public/dateimages/deaddry/21-11-08 13-06-02/"
imagefiles = dir(strcat(srcPath,'*.bmp'));      
nfiles = length(imagefiles);    % Number of files found
% for ii=1:nfiles
%    currentfilename = imagefiles(ii).name;
%    path =strcat( srcPath,currentfilename);
%    I = imread(path);
%    
%    greenMask=hsvMaskS(I)
%    I1 = I .* uint8(greenMask);
%    grayI=rgb2gray(I1)
%    mask=morph(grayI)
%    nexttile
%    imshowpair(I,mask,"blend")
% end

for ii=1:nfiles
   currentfilename = imagefiles(ii).name;
   path =strcat( srcPath,currentfilename);
   oI = imread(path);
   
    ycbcrMk=yCbCrMask(oI)
    hsvMK=hsvMask(oI)
    rgbMK=rgbMask(oI)
    ychsFuse=imfuse(ycbcrMk,hsvMK,"blend")
    fullFuse=imfuse(ychsFuse,rgbMK,"blend")
    mask=morph2(fullFuse)
    

   nexttile
   imshowpair(oI,mask,"blend")
end