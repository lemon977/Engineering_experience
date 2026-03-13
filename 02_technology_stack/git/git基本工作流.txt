Git 新手完全指南（一步到位）

【第一步】安装与配置（电脑只需做一次）
----------------------------------

Windows安装：
winget install --id Git.Git -e --source winget

Linux安装：
sudo apt update && sudo apt install git -y

验证：
git --version

配置身份（必须）：
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"


【第二步】GitHub创建仓库（网页操作）
----------------------------------

1. 登录 github.com → 右上角 + → New repository
2. 填写仓库名
3. ⚠️ 不要勾选 "Add a README file"
4. 创建后复制仓库地址（如 https://github.com/用户名/仓库名.git）


【第三步】本地初始化（每个项目一次）
----------------------------------

进入项目文件夹：
cd 你的项目路径

初始化：
git init

创建README：
echo "# 项目名" > README.md

添加并提交：
git add .
git commit -m "init: 初始化项目"


【第四步】关联远程并推送（每个项目一次）
----------------------------------

关联远程：
git remote add origin https://github.com/用户名/仓库名.git

验证：
git remote -v

推送：
git push -u origin main


【第五步】日常开发（每天重复）
----------------------------------

拉取最新：
git pull origin main

查看变更：
git status

添加提交：
git add .     (指定项目提交：git add 具体项目名)
git commit -m "feat: 描述做了什么"

推送：
git push


【避坑清单】
----------------------------------
✓ 先本地init再关联，不要先建带README的远程仓库
✓ 每次commit写清楚描述（feat:/fix:/update:）
✓ 推送前先pull
✓ 不确定时先git status查看状态