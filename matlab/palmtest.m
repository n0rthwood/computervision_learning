srcPath="zebraimg/"
imagefiles = dir(strcat(srcPath,'*.bmp'));      
nfiles = length(imagefiles);    % Number of files found
for ii=1:nfiles
   currentfilename = imagefiles(ii).name;
   path =strcat( srcPath,currentfilename);
   currentimage = imread(path);

   mask = palm(currentimage)
   result = imfuse(currentimage,imresize(mask,10),'blend')
   imshow(result)
   waitforbuttonpress
end