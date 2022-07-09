imagefiles = dir('D:\tmp\21-11-09 09-34-06-cam0-fardh-扣枣优化\21-11-09 09-34-06\*.bmp');      
nfiles = length(imagefiles);    % Number of files found
for ii=1:nfiles
   currentfilename = imagefiles(ii).name;
   path =strcat( 'D:\tmp\21-11-09 09-34-06-cam0-fardh-扣枣优化\21-11-09 09-34-06\',currentfilename);
   RGB = imread(path);
   
   
he=RGB
lab_he = rgb2lab(he);
ab = lab_he(:,:,2:3);
ab = im2single(ab);

nColors = 2;
% repeat the clustering 3 times to avoid local minima
pixel_labels = imsegkmeans(ab,nColors,'NumAttempts',1);

% for ii=1:2
mask2 = pixel_labels==1;
cluster2 = he .* uint8(mask2);
imshow(cluster2)
waitforbuttonpress
end
% end


%RGB=imread("a.bmp")
