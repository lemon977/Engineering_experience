基础安装

1.安装 Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
2.下载 Miniconda 安装脚本
chmod +x Miniconda3-latest-Linux-x86_64.sh
3.给脚本添加执行权限(安装到指定目录（无交互安装）)
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
4.初始化
$HOME/miniconda3/bin/conda init
5.把 conda 加入 shell 环境
source ~/.bashrc

基础配置

关闭 base 环境自动激活
conda config --set auto_activate_base false
添加常用软件源（更全）
conda config --add channels conda-forge
优先使用已配置的软件源
conda config --set channel_priority strict
更新 conda 本身
conda update -n base -c defaults conda

基础使用

创建名为 robot 的 Python 3.10 环境
conda create -n robot python=3.10
进入该环境
conda activate robot
查看所有环境
conda env list
删除环境
conda remove -n robot --all
导出当前环境配置
conda env export > environment.yml
根据配置文件创建环境
conda env create -f environment.yml

 说明
---
* 不在 base 环境开发
* ROS 使用系统 Python
* Conda 用于独立环境
---
