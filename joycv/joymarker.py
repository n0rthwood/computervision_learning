import cv2
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from features import double
from util import io
from morph import morph
from joycv.features import basic
import config
print('temp_path: '+config.temp_path)
plt.rcParams['figure.figsize'] = (15, 10)
plt.rcParams['figure.dpi'] = 100

images,masks,image_names_list = io.load_image_from_folder('../testbmp/',True, '*')
start_time = datetime.now()
debug_list={};

debug_list = {
   "cc9.bmp":[(0,4)],
    "cc8.bmp":[(2,3),(2,1)],
    "cc11.bmp":[(0,3),(2,5),(1,5),(3,2),(3,4)],
    "ajwa2.bmp":[(3,3),(1,1)],
    "fd1.bmp":[(2,5),(1,2),(1,4)],
"fd2.bmp":[(2,5),(3,5),(3,1),(0,2),(1,2)],
    "dd1.bmp":[(0,1)],
    "dd2.bmp":[(1,5)],
   "dd4.bmp": [(2, 5)],
              }

# create a morphed mask list same size as images
morphed_masks = [morph.close_and_open(mask,5,28) for mask in masks]

#apply morphed mask to images
morphed_images = [cv2.bitwise_and(image,image,mask =morphed_mask ) for image,morphed_mask in zip(images,morphed_masks)]

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
print('Image count {}'.format(len(images)))

sliced_image_list,sliced_mask_list =  io.slice_by_grid_batch(images,morphed_masks,slice_grid_row_column=[4,6])
for i in range(len(sliced_image_list)):
   sliced_images = sliced_image_list[i];
   sliced_masks = sliced_mask_list[i];

   #plt.figure()
   f, ax = plt.subplots(4, 6)
   f.suptitle(image_names_list[i],fontsize=30)
   subImages=[]
   if image_names_list[i] in debug_list.keys():
      subImages=debug_list[image_names_list[i]]
   axarr = ax.flat
   pltindex = 0
   for j in range(len(sliced_images)):
      sliced_image = sliced_images[j];
      sliced_mask = sliced_masks[j];
      contours =  basic.find_contours(sliced_mask)
      exist = basic.find_existance(contours)
      debug_label='';
      if(exist):
         debug_flag=False;
         for debug_corrd in subImages:
            if(debug_corrd[0]==j//6 and debug_corrd[1]==j%6):
               debug_flag = True;
         width, height, rect,contour_max,left,right,top,bottom = basic.find_size(contours)
         color = basic.find_color(sliced_image,sliced_mask)
         #sliced_mask_channel_expanded= cv2.cvtColor(sliced_mask,cv2.COLOR_GRAY2RGB)

         double_count,subfig = basic.find_double_skiimage(sliced_mask)
         debug_label=basic.draw_debug_info(sliced_image,contour_max,left,right,top,bottom,width,height,color,double_count)
         if (debug_flag):
            np.save(
               config.temp_path + image_names_list[i].rsplit(".", 1)[0] + '_sliced_mask_' + str(j // 6) + '_' + str(
                  j % 6) + '.npy', sliced_mask)
            subfig.savefig(
               config.temp_path + image_names_list[i].rsplit(".", 1)[0] + '_sliced_mask_' + str(j // 6) + '_' + str(
                  j % 6) + '.png')
            plt.close(subfig)
      even_num_j = j%2
      if(even_num_j == 0):
         end_line_return ='\n'
         start_line_return =''
      else:
         start_line_return ='\n'
         end_line_return =''
      axarr[pltindex].imshow(sliced_image)
      axarr[pltindex].set_title(str(j//6)+'-'+str(j%6)+start_line_return+'\n'+debug_label+end_line_return,fontsize=10)
      axarr[pltindex].axis('off')
      pltindex += 1
   #plt.show()
   f.savefig(config.temp_path+image_names_list[i].rsplit( ".", 1 )[ 0 ]+'.png')
   print('Saved: '+config.temp_path+image_names_list[i].rsplit( ".", 1 )[ 0 ]+'.png')
   plt.close(f)
#
# type_of_images = 3;
# no_of_image_per_row = 3;
# show_panel_row_count = no_of_image_per_row*type_of_images;
#
# pltindex = 0;
# f, ax = plt.subplots( len(images)//no_of_image_per_row ,show_panel_row_count )
# axarr = ax.flat
# for i in range(len(morphed_images)):
#         axarr[pltindex].imshow(images[i])
#         axarr[pltindex].axis('off')
#         axarr[pltindex].set_title(str(i)+'-'+str(pltindex%(i+1)))  # get the title property handler
#         pltindex+=1
#         axarr[pltindex].imshow(morphed_masks[i])
#         axarr[pltindex].axis('off')
#         axarr[pltindex].set_title(
#             str(i ) + '-' + str(pltindex%(i+1)))  # get the title property handler
#         pltindex += 1
#         axarr[pltindex].imshow(morphed_images[i])
#         axarr[pltindex].axis('off')
#         axarr[pltindex].set_title(
#             str(i ) + '-' + str(pltindex%(i+1)))  # get the title property handler
#         pltindex += 1
# plt.show()

#
# gray_final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
# ret, gray_final = cv2.threshold(gray_final, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
# src1_mask = cv2.cvtColor(mmorphed_mk, cv2.COLOR_GRAY2BGR)  # change mask to a 3 channel image
# mask_out = cv2.subtract(src1_mask, image)
# mask_out = cv2.subtract(src1_mask, mask_out)

#
# correct_color = image
#
# end_time = datetime.now()
# print('Duration: {}'.format(end_time - start_time))
#
# # slice image into 4*6 grid and display
# h, w, c = mask_out.shape
# grid = [4, 6]
# f, ax = plt.subplots(4, 6)
# axarr = ax.flat
# grid_h = h // grid[0]
# grid_w = w // grid[1]
# grid_images = [];
# pltindex = 0;
# for i in range(grid[0]):
#     for j in range(grid[1]):
#         sliced_img = correct_color[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w];
#         sliced_mask = mmorphed_mk[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w];
#         double_check_mask = cv2.cvtColor(sliced_mask, cv2.COLOR_GRAY2RGB);
#
#         contours, hierarchy = cv2.findContours(sliced_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#         cv2.drawContours(sliced_img, contours, -1, (255, 0, 0), 3)
#
#         if len(contours) != 0:
#             double_count, thresh, opening, sure_bg, dist_transform, sure_fg, unknown_area, markers = double.check_double(
#                 double_check_mask)
#             c = max(contours, key=cv2.contourArea, default=0)
#             left = tuple(c[c[:, :, 0].argmin()][0])
#             right = tuple(c[c[:, :, 0].argmax()][0])
#             top = tuple(c[c[:, :, 1].argmin()][0])
#             bottom = tuple(c[c[:, :, 1].argmax()][0])
#
#             cv2.drawContours(sliced_img, [c], -1, (36, 255, 12), 2)
#             cv2.circle(sliced_img, left, 8, (0, 50, 255), -1)
#             cv2.circle(sliced_img, right, 8, (0, 255, 255), -1)
#
#             cv2.circle(sliced_img, top, 8, (255, 50, 0), -1)
#             cv2.circle(sliced_img, bottom, 8, (255, 255, 0), -1)
#
#             YCrCb_mean = cv2.mean(cv2.cvtColor(sliced_img, cv2.COLOR_RGB2YCrCb), sliced_mask)
#
#             h, w, ccoo = sliced_img.shape
#             cv2.rectangle(sliced_img, (left[0], top[1]), (right[0], bottom[1]), (255, 0, 0), 2)
#             cv2.putText(sliced_img,
#                         'w:' + str(right[0] - left[0]) + ' h:' + str(bottom[1] - top[1]) + ' c[0-255]:' + str(
#                             round(YCrCb_mean[0])) + ' d:' + str(double_count), (2, h - 5), cv2.FONT_HERSHEY_SIMPLEX,
#                         0.5, (255, 0, 0), 1, cv2.LINE_AA)
#         grid_images.append(sliced_img)
#         axarr[pltindex].imshow(sliced_img)
#         axarr[pltindex].axis('off')
#         title_obj = axarr[pltindex].set_title('' + str(i) + str("-") + str(j))  # get the title property handler
#
#         # print(pltindex)
#         pltindex += 1
#
# plt.show()

exit()
# cv2.waitKey(0)


# load image from a folder and loop through all images in the folder