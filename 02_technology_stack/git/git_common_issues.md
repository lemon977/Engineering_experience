【快速索引】输入编号跳转到对应问题
----------------------------------

推送相关：P1-P3
  P1 推送被拒绝(fetch first)
  P2 拒绝合并不相关历史
  P3 每次推送要输密码

提交相关：C1-C3
  C1 提交信息写错了
  C2 漏加文件到上次提交
  C3 提交了敏感信息

撤销回退：R1-R4
  R1 撤销工作区修改
  R2 撤销暂存区文件
  R3 已经add和commit，撤销提交
  R4 回退到某个版本
  R5 回退后想恢复

分支相关：B1-B6
  B1 查看所有分支
  B2 创建并切换新分支
  B3 切换分支
  B4 合并分支到main
  B5 删除本地分支
  B6 删除远程分支

冲突相关：M1-M2
  M1 pull时冲突
  M2 放弃合并

远程仓库：O1-O4
  O1 查看远程地址
  O2 修改远程地址
  O3 添加多个远程
  O4 忘记关联远程

文件相关：F1-F3
  F1 误删文件恢复
  F2 删除已提交的大文件
  F3 忽略文件不生效

其他高频：X1-X6
  X1 中文文件名乱码
  X2 换行符问题
  X3 查看文件修改历史
  X4 比较差异
  X5 暂存当前修改
  X6 强制推送

致命恢复：D1-D3
  D1 执行reset --hard后恢复
  D2 删除整个本地仓库
  D3 误删.git文件夹


==================================
详细解答
==================================

【P1】推送被拒绝 ! [rejected] main -> main (fetch first)
原因：远程仓库有本地没有的内容（如README）
解决：
git pull origin main --rebase
git push -u origin main

【P2】提示 refusing to merge unrelated histories
原因：本地和远程仓库历史完全不相关
解决：
git pull origin main --allow-unrelated-histories
# 解决冲突后提交推送

【P3】每次推送都要输入密码
原因：使用了HTTPS但没有配置凭证管理
解决（任选一种）：
- 使用SSH方式关联远程仓库
- 或：git config --global credential.helper store
- 或：Windows安装Git Credential Manager


【C1】提交信息写错了
解决（未推送时）：
git commit --amend -m "正确的提交信息"

【C2】漏加了文件到上次提交
解决：
git add 漏掉的文件
git commit --amend --no-edit

【C3】不小心提交了敏感信息（密码/密钥）
解决：
git reset --soft HEAD~1
git restore --staged 敏感文件
git restore 敏感文件
# 修改.gitignore后重新提交


【R1】想撤销工作区的修改（未add）
git restore 文件名
git restore . （撤销所有）

【R2】想撤销暂存区的文件（已add未commit）
git restore --staged 文件名

【R3】已经add和commit，想撤销这次提交（保留修改）：
git reset --soft HEAD~1

【R4】想回退到某个版本
查看历史：
git log --oneline
回退：
git reset --hard 版本号前几位

【R5】回退后想恢复
git reflog
git reset --hard 之前的版本号


【B1】查看所有分支
git branch -a

【B2】创建并切换新分支
git checkout -b 新分支名

【B3】切换分支
git checkout 分支名

【B4】合并分支到main
git checkout main
git pull origin main
git merge 要合并的分支
git push

【B5】删除本地分支
git branch -d 分支名
强制删除：
git branch -D 分支名

【B6】删除远程分支
git push origin --delete 分支名


【M1】pull时提示冲突 CONFLICT
解决：
1. 打开冲突文件，找到 <<<<<<< ======= >>>>>>> 标记
2. 手动编辑保留需要的代码，删除标记
3. git add .
4. git commit -m "fix: 解决合并冲突"
5. git push

【M2】想放弃合并，回到合并前
git merge --abort


【O1】查看远程仓库地址
git remote -v

【O2】修改远程仓库地址
git remote set-url origin 新地址

【O3】添加多个远程仓库
git remote add 别名 地址
git push 别名 分支名

【O4】忘记关联远程仓库就推送
提示：fatal: No configured push destination
解决：
git remote add origin 仓库地址
git push -u origin main


【F1】文件被误删，想恢复
git restore 文件名

【F2】大文件不小心提交，想彻底删除
git rm --cached 大文件
echo "大文件名" >> .gitignore
git commit -m "remove: 删除大文件"
git push

【F3】忽略文件不生效（已track的文件）
git rm -r --cached .
git add .
git commit -m "fix: 更新.gitignore"


【X1】中文文件名显示乱码
git config --global core.quotepath false

【X2】Windows换行符问题（LF/CRLF）
git config --global core.autocrlf true

【X3】查看某文件修改历史
git log -p 文件名

【X4】比较差异
工作区vs暂存区：git diff
暂存区vs上次提交：git diff --staged

【X5】暂存当前修改（临时切换分支）
git stash
git stash list
git stash pop （恢复）

【X6】强制推送（慎用！会覆盖远程）
git push --force
或安全方式：
git push --force-with-lease


【D1】执行了git reset --hard，代码没了
恢复：
git reflog
找到reset前的版本号
git reset --hard 那个版本号

【D2】删除了整个本地仓库
恢复：从GitHub重新clone
git clone 仓库地址

【D3】误删了.git文件夹
恢复：从GitHub重新clone，手动复制文件过去