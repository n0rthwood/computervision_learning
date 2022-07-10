srcPath="fardimg/"
imagefiles = dir(strcat(srcPath,'*.bmp'));      
nfiles = length(imagefiles);    % Number of files found
for ii=1:nfiles
   currentfilename = imagefiles(ii).name;
   path =strcat( srcPath,currentfilename);
   currentimage = imread(path);

   mask = palm(imresize(currentimage,0.5))
   figure
   result = imfuse(currentimage,imresize(mask,2),'blend')
   imshow(result)
   waitforbuttonpress
end