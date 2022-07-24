% l1=imread("/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/lulu2_sliced_image_3_2.png");
% l2=imread("/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/lulu2_sliced_image_0_5.png");
% l3=imread("/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/lulu2_sliced_image_1_4.png");
% l4=imread("/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/lulu2_sliced_image_2_5.png");
% 
% image=l4;
% mask=lulu_color(image);
% f=bsxfun(@times,image,cast(mask,'like',image));
% imshow(f);

c1=imread("/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/hn1_sliced_image_2_3.png");
gray=rgb2gray(c1);

imshow(gray)