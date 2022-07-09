function [BW,maskedImage] = segmentImage(RGB)
%----------------------------------------------------

he=RGB
lab_he = rgb2lab(he);
ab = lab_he(:,:,2:3);
ab = im2single(ab);

nColors = 2;
% repeat the clustering 3 times to avoid local minima
pixel_labels = imsegkmeans(ab,nColors,'NumAttempts',1);

mask2 = pixel_labels==1;
cluster2 = he .* uint8(mask2);

% Convert RGB image into L*a*b* color space.
X = rgb2lab(cluster2);

% Create empty mask.
BW = false(size(X,1),size(X,2));

% 泛洪填充
row = 107;
column = 178;
tolerance = 5.000000e-02;
normX = sum((X - X(row,column,:)).^2,3);
normX = mat2gray(normX);
weightImage = graydiffweight(normX, column, row, 'GrayDifferenceCutoff', tolerance);
addedRegion = imsegfmm(weightImage, column, row, 0.01);
BW = BW | addedRegion;

% 使用 disk 执行掩膜开运算
radius = 24;
decomposition = 8;
se = strel('disk', radius, decomposition);
BW = imopen(BW, se);

% Create masked image.
maskedImage = RGB;
maskedImage(repmat(~BW,[1 1 3])) = 0;
end

