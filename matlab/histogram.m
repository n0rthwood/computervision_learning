I=imread('a.bmp');        %读取当前路径下的图片
I1=rgb2gray(I);
figure;
subplot(2,2,1);
imshow(I1);
title(' 灰度图像')
region=[50,300,50,200]

thresh1=65
thresh2=40

axis(region);   %坐标轴的起始值
grid on;                       %显示网格线
axis on;                     %显示坐标系
[m,n]=size(I1);                            %测量图像尺寸参数
GK=zeros(1,256);                           %预创建存放灰度出现概率的向量
for k=0:255
     GK(k+1)=length(find(I1==k))/(m*n);    %计算每级灰度出现的概率，将其存入GK中相应位置
end
subplot(2,2,2),bar(0:255,GK,'g')                   %绘制直方图
title('灰度直方图')
xlabel('灰度值')
ylabel(' 出现概率')
I2=im2bw(I,thresh1/255);  
subplot(2,2,3),imshow(I2);
title(strcat('阈值',thresh1,'的分割图像'))
axis(region);
grid on;                  %显示网格线
axis on;                  %显示坐标系
I3=im2bw(I,thresh2/255);   %
subplot(2,2,4),imshow(I3);
title(strcat('阈值',thresh2,'的分割图像'))
axis(region);
grid on;                  %显示网格线
axis on;                  %显示坐标系
