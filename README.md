# NanoDCALTool
A toolkit for NanoDCAL, including xml reading...

## install

Here we choose the conda to install the environment depended.

- create conda environment

    ``` bash
    $ conda create -n deepDH python=3.9
    ```
- active environment

    ``` bash
    $ conda activate deepDH
    ```
- install requirements
    ``` bash
    $ conda activate deepDH
    # 
    $ conda install --yes --file requirements.txt
    # or install with pip, if you like you can add " -i https://pypi.tuna.tsinghua.edu.cn/simple" to use a mirror in China
    $ pip install -r requirements.txt 
    ```

## usage
``` bash
$ python main.py --xml_i='./example/testPY/Transmission.xml' --auto
```

将`Transmission.xml`数据读出来, 并转化为`Python`格式, 并储存在`npz`文件中. 
如果是数组是二维数组将会以txt格式明文储存.

如果有`coordinatesOfKPoints`数据, 会把`k`点映的定义域射到关于`0`点对称的范围, 
如$(0,2 \pi) \to (-\pi,\pi)$. 坐标储存在`transm.coordinatesOfKPoints_transpose_shift.dat`文件中.



