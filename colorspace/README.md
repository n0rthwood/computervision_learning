先安装python
然后，最好创建一个虚拟环境,免得你的本地环境里面有乱七八糟的东西，引起引用冲突
```bash
python -m venv /path/to/venv
```

创建虚拟环境后，激活虚拟环境

```bash
source /path/to/venv/bin/activate
```

用pip安装所需的库

```bash
pip install -r requirements.txt
```

运行程序

```bash
python test.py
```

修改代码里面的图片路径尝试不同效果
```fd1.bmp,fullcategory.png,zb1.bmp,cc11.bmp,dd1.bmp```

颜色好像是BGR不是RGB，不过我也没再折腾