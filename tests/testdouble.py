import joycv.features.double as double
import numpy as np
from matplotlib import pyplot as plt
import tempfile
from pathlib import Path

root_path='/var/folders/1v/scs78_j96pd1shbpfsdmm1rw0000gn/T/joycv_tmp/';
save_path=root_path+'double/';
Path(save_path).mkdir(parents=True, exist_ok=True)

image_data_path=[
'fd2_sliced_mask_1_2.npy','fd2_sliced_mask_3_5.npy','fd1_sliced_mask_2_5.npy',
    'dd1_sliced_mask_0_1.npy','ajwa2_sliced_mask_3_3.npy',
    'cc5_sliced_mask_1_4.npy','cc10_sliced_mask_2_4.npy','cc6_sliced_mask_2_4.npy',
]

result_data=[];
expected_ressult=[1,    1,    2,    1,1,2,1,2];
for path in (image_data_path):
   image= np.load(root_path+path,allow_pickle=True)
   count, fig = double.check_double_skiimage(image, debug=True)
   result_data.append(count)
   fig.savefig(save_path+path+'.png')
   plt.close(fig)
   #print(path+': '+str(count))

for expected_index in range(len(expected_ressult)):
    if expected_ressult[expected_index] != result_data[expected_index]:
        print('Error: expected '+str(expected_ressult[expected_index])+' but got '+str(result_data[expected_index]))
    else:
        print(' '+str(expected_ressult[expected_index])+'= '+str(result_data[expected_index]))