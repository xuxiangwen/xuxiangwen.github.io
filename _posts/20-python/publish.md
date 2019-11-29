本文例子来自[创建并发布自己的python模块](https://www.jianshu.com/p/905156486d79)

## 1. 创建模块

~~~
mkdir eipi10_pkg_sample
cat << EOF > eipi10_pkg_sample/nestList.py

"""
模块示例
可以打印嵌套列表
"""

__author__ = 'eipi10'

# indent表示缩进，默认0表示无缩进
def print_list(lst, indent = 0):
    for item in lst:
        # 判断列表lst中的每一项是否是list对象，
        # 如果是则递归调用print_list，同时缩进级别加1
        if isinstance(item, list):   
            print_list(item, indent + 1)
        else:
            print("--" * indent, end="")
            print(item)
            
if __name__ == '__main__':
    alist = ['michael', 'rosa', ['xu', ['xiang', 'wen'], 'long']]
    print_list(alist)

EOF

cat << EOF > eipi10_pkg_sample/__init__.py
name = "example_pkg_zx1"

EOF


~~~



## 2. 发布模块

### 构建前的准备

~~~
cat << EOF > README.md
# Example Package

nestList.py是一个可以打印缩进列表的示例函数,示例代码如下：

    from eipi10_pkg_sample import nestList
    alist = ["grace", "angle", "roy", 
                ["anna", "jhon", "richard", ["nio", "lily"]], 
                "bluce"]        
    nestList.print_list(alist)


EOF

cat  << EOF > LICENSE
Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

EOF


cat << EOF > setup.py
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eipi10_pkg_sample",
    version="0.0.2",
    author="eipi10",
    author_email="eipi10@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xuxiangwen/xuxiangwen.github.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

EOF
~~~

- name参数在上传到internet上要求必须是唯一的，不能有重复，否则无法上传

### 构建发布文件

确保安装了 setuptools和wheel

~~~
pip install --user --upgrade setuptools wheel
~~~

开始构建

~~~python
rm -rf dist
python3 setup.py sdist bdist_wheel
~~~

构建完成后会创建多个文件及目录，其中dist目录下会生成.whl和.tar.gz两个文件.



## 3. 上传模块到PyPI(Python Package Index)

接下来把自己的模块分享到internet上，让全球的程序员都能使用你贡献的代码。由于本文只是一个tutorial，所以不使用正式的平台，而是使用一个测试平台Test Pypi。

1. 在[Test PyPI页面](https://test.pypi.org/account/register/)进行注册。

   eipi10/QA...02

2. 安装twine

   ~~~
   pip install --user --upgrade twine
   ~~~

3. 上传

   ~~~
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   ~~~

4. 安装

   ~~~
   pip install -U -i https://test.pypi.org/simple/ eipi10-pkg-sample
   ~~~

如果是已经完全准备好了，可以把模块发布到正式环境。

1. [https://pypi.org](https://pypi.org/)上注册正式的账户并验证邮箱。

   eipi10/QA...02

2. 上传

   ~~~
   twine upload dist/*
   ~~~

3. 安装

   ~~~
   pip install -U your-package-nam
   ~~~

   

## 代码汇总

~~~
cd <floder>
rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload dist/*
~~~

