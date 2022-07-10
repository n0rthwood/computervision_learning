srcPath="/Users/bill/Documents/MATLAB/computervision_learning/matlab/fardimg/"
imagefiles = dir(strcat(srcPath,'*.bmp'));      
nfiles = length(imagefiles);    % Number of files found
for ii=1:nfiles
   currentfilename = imagefiles(ii).name;
   path =strcat( srcPath,currentfilename);
   I = imread(path);
   
   greenMask=hsvMaskS(I)
   I1 = I .* uint8(greenMask);
   grayI=rgb2gray(I1)
   mask=morph(grayI)
   nexttile
   imshowpair(I,mask,"blend")
end

