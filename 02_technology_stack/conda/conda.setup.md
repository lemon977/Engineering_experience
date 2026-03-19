1. 下载
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
2. 给权限（不需要 sudo）
chmod +x Miniconda3-latest-Linux-x86_64.sh
3. 安装（指定路径）
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
4. 初始化
$HOME/miniconda3/bin/conda init
5. 重新加载 shell
source ~/.bashrc