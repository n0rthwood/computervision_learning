srcPath="../testbmp/"
imagefiles = dir(strcat(srcPath,'*.bmp'));      
nfiles = length(imagefiles);    % Number of files found
for ii=1:nfiles
   currentfilename = imagefiles(ii).name;
   path =strcat( srcPath,currentfilename);
   oI = imread(path);
   joyseg(oI);
end