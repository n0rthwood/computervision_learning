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
   "fd3.bmp": [(2, 1)],
    "dd1.bmp":[(0,1)],
    "dd2.bmp":[(1,5)],
   "dd4.bmp": [(2, 5)],
   "cc5.bmp": [(1, 4)],
   "cc10.bmp": [(2, 4)],
    "cc6.bmp": [(2, 4)],
    "cc12.bmp": [(1, 4)],
   "khs1.bmp": [(2, 4),(2,5),(3,4)],
   "cc_s3.bmp": [(0, 3),(0,5),(1,2),(1,4),(1,5),(2,3),(3,5)],
   "cc_s1.bmp": [(0, 5),(1,4),(2,3),(2,5),(3,2),(3,4),(3,5)],
   "lulu1.bmp": [(0, 5),(1,4),(2,3),(2,5),(3,2),(3,4),(3,5)],
   "lulu2.bmp": [(0, 5), (1, 4), (2, 3), (2, 5), (3, 2), (3, 4), (3, 5)],
   "lulu3.bmp": [(0, 4), (0, 5), (1, 4), (1, 5),(2, 4), (2, 5),(3, 4), (3, 5),],
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
      osi=sliced_image.copy();
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
            np.save(config.temp_path + image_names_list[i].rsplit(".", 1)[0] + '_sliced_mask_' + str(j // 6) + '_' + str( j % 6) + '.npy', sliced_mask, allow_pickle=True)
            cv2.imwrite(config.temp_path + image_names_list[i].rsplit(".", 1)[0] + '_sliced_image_' + str(j // 6) + '_' + str( j % 6) + '.png', cv2.cvtColor(basic.extract_img(osi,sliced_mask),cv2.COLOR_BGR2RGB))
            #subfig.savefig( config.temp_path + image_names_list[i].rsplit(".", 1)[0] + '_sliced_mask_' + str(j // 6) + '_' + str( j % 6) + '.png')
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

exit()
