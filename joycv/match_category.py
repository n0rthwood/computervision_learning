import os
from pathlib import Path
import shutil

categories_path= "/Users/bill/Downloads/aprin/730-training/sliced_image/"
to_be_categoried_path= "/Users/bill/Downloads/aprin/out/sliced_image/sm3"
out_path = "/Users/bill/Downloads/aprin/recat"

cats=[]
for root, dirs, cat_files in os.walk(categories_path):
    if os.path.normpath(categories_path) == os.path.normpath(root):
        continue

    cat_files=[file.split("_s5")[0]+".png" for file in cat_files]
    cats.append(root.split("/")[-1])
    print(root, dirs, cat_files)


for tb_root,dir,tb_files in os.walk(to_be_categoried_path):
    for cat in cats:
        cat_path = os.path.join(out_path, cat)
        Path(cat_path).mkdir(parents=True, exist_ok=True);
        print("process category: {}".format(cat))
        for tb_file in tb_files:
            src=os.path.join(tb_root,tb_file)
            dst=os.path.join(cat_path,tb_file)
            shutil.copyfile(src, dst)



