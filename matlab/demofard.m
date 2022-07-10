% srcPath="Y:\zebra\21-11-07 17-44-18-cam1-zebra\21-11-07 17-44-18\"
% imagefiles = dir(strcat(srcPath,'*.bmp'));      
% nfiles = length(imagefiles);    % Number of files found
% for ii=1:nfiles
%    currentfilename = imagefiles(ii).name;
%    path =strcat( srcPath,currentfilename);
%    currentimage = imread(path);
% 
%    mask = segmentImageResize(currentimage)
%    result = imfuse(currentimage,imresize(mask,10),'blend')
%    imshow(result)
%    waitforbuttonpress
% end
i = imread("d.bmp")

mask = segmentImageTh(i)
imshowpair(i,mask,"blend")
