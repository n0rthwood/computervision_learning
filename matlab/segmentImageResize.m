function [BW,maskedImage] = segmentImageResize(X)
%segmentImage Segment image using auto-generated code from imageSegmenter app
%  [BW,MASKEDIMAGE] = segmentImage(X) segments image X using auto-generated
%  code from the imageSegmenter app. The final segmentation is returned in
%  BW, and a masked image is returned in MASKEDIMAGE.

% Auto-generated by imageSegmenter app on 09-Jul-2022
%----------------------------------------------------

he=imresize(X,0.1)
lab_he = rgb2lab(he);
ab = lab_he(:,:,2:3);
ab = im2single(ab);

nColors = 2;
% repeat the clustering 3 times to avoid local minima
pixel_labels = imsegkmeans(ab,nColors,'NumAttempts',1);

mask2 = pixel_labels==1;
cluster2 = he .* uint8(mask2);
X=rgb2gray(cluster2)


% Create empty mask.
BW = false(size(X,1),size(X,2));

% 阈值化图像 - 全局阈值
BW = imbinarize(X);

% 填充孔
BW = imfill(BW, 'holes');

% 反转掩膜
BW = imcomplement(BW);

% 使用 disk 执行掩膜开运算
radius = 3;
decomposition = 8;
se = strel('disk', radius, decomposition);
BW = imopen(BW, se);

% Create masked image.
maskedImage = X;
maskedImage(~BW) = 0;
end

