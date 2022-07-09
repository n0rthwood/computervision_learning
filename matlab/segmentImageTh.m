function [BW,maskedImage] = segmentImageTh(X)
%segmentImage Segment image using auto-generated code from imageSegmenter app
%  [BW,MASKEDIMAGE] = segmentImage(X) segments image X using auto-generated
%  code from the imageSegmenter app. The final segmentation is returned in
%  BW, and a masked image is returned in MASKEDIMAGE.

% Auto-generated by imageSegmenter app on 09-Jul-2022
%----------------------------------------------------

he=X
lab_he = rgb2lab(he);
ab = lab_he(:,:,2:3);
ab = im2single(ab);

nColors = 2;
% repeat the clustering 3 times to avoid local minima
pixel_labels = imsegkmeans(ab,nColors,'NumAttempts',10);

mask2 = pixel_labels==1;
cluster2 = he .* uint8(mask2);
imshow(cluster2)
waitforbuttonpress
X=rgb2gray(cluster2)


% Create empty mask.
BW = false(size(X,1),size(X,2));

% 阈值化图像 - 自适应阈值
BW = imbinarize(X, 'adaptive', 'Sensitivity', 0.000000, 'ForegroundPolarity', 'dark');

% 使用 disk 腐蚀掩膜
radius = 7;
decomposition = 8;
se = strel('disk', radius, decomposition);
BW = imerode(BW, se);

% 使用 disk 膨胀掩膜
radius = 19;
decomposition = 8;
se = strel('disk', radius, decomposition);
BW = imdilate(BW, se);

% 反转掩膜
BW = imcomplement(BW);

% 使用 disk 执行掩膜开运算
radius = 22;
decomposition = 8;
se = strel('disk', radius, decomposition);
BW = imopen(BW, se);

% 使用 disk 膨胀掩膜
radius = 13;
decomposition = 8;
se = strel('disk', radius, decomposition);
BW = imdilate(BW, se);

% Create masked image.
maskedImage = X;
maskedImage(~BW) = 0;
end

