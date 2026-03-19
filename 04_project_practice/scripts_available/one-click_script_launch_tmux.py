#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键启动多终端演示脚本（含自动输密码 agx）
依赖：tmux
用法:
  ./start_demo.py          # 启动
  ./start_demo.py -k       # 仅清场
"""

# ==================== 标准库导入 ====================
import argparse      # 【重点1】命令行参数解析，用 -k 这种短选项就靠它
import subprocess    # 【重点2】执行 shell 命令，替代 os.system
import time          # 延时等待
from pathlib import Path  # 【重点3】现代化路径处理，比字符串拼接路径好用

# ==================== 配置常量 ====================
SESSION   = "piper_demo"   # tmux 会话名，改这里就能改会话名
PKG_ROOT  = Path.home() / "cobot_magic/Piper_ros_private-ros-noetic"  # ~ 自动展开
DEMO_ROOT = "/home/agilex/Manipulation_Demo_smooth"  # 绝对路径也行
LOG_DIR   = Path.home() / "piper_logs"  # Path 对象支持 / 拼接路径

# 【重点4】JOBS 列表：核心数据结构，(名称, 命令) 元组列表
# 关键：第二条命令里自动喂密码 agx 给 sudo
JOBS = [
    # 简单命令直接写字符串
    ("00_roscore",     "roscore"),
    
    # 【重点5】f-string 嵌入变量和命令，echo 密码 | sudo -S 自动输入
    ("01_can_config",  f"cd {PKG_ROOT} && echo agx | sudo -S ./can_config.sh"),
    
    # 组合命令用 && 连接
    ("02_realsense",   f"cd {PKG_ROOT} && roslaunch realsense2_camera multi_camera.launch"),
    
    ("03_piper",       f"cd {PKG_ROOT} && roslaunch piper start_ms_piper.launch mode:=1 auto_enable:=true"),
    
    # 【重点6】长命令分行：用括号包裹，f-string 自动拼接
    ("04_inference",   f"cd {DEMO_ROOT} && "
                       f"exec bash -c 'source ~/miniconda3/etc/profile.d/conda.sh && "
                       f"conda activate aloha_pi0_py310 && "
                       f"export PYTHONPATH={DEMO_ROOT}/packages/openpi-client/src:$PYTHONPATH && "
                       f"python agilex_inference_openpi_smooth_auto_reset.py --host 172.10.1.50 --port 8001 "
                       f"--ctrl_type joint --use_temporal_smoothing --chunk_size 50'"),
]

# 【重点7】lambda 定义快捷函数，比 def 简洁，适合简单包装
# chk=True 表示命令失败时抛异常（check 的缩写）
run = lambda cmd, chk=True: subprocess.run(cmd, shell=True, check=chk)

def kill_session():
    """清理已存在的 tmux 会话"""
    # chk=False 因为会话可能不存在，不报错
    run(f"tmux kill-session -t {SESSION} 2>/dev/null", chk=False)

def main():
    # 【重点8】argparse 标准模板：创建、加参数、解析
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--kill-only", action="store_true", help="仅清场")
    args = parser.parse_args()  # 解析后的参数在 args 对象里

    # 【重点9】根据参数分支：if args.xxx 判断用户输入了什么
    if args.kill_only:
        kill_session()
        print("✅ 已清理 tmux session")
        return  # 直接结束，不执行后面

    # Path 对象的方法：自动创建目录（包括父目录），已存在不报错
    LOG_DIR.mkdir(exist_ok=True)
    kill_session()  # 先清场，避免冲突

    # ==================== tmux 布局创建 ====================
    # 【重点10】窗格布局：先创建，再分割，最后调整布局
    
    run(f"tmux new-session -d -s {SESSION}")   # -d 后台创建，不立即附着
    run(f"tmux split-window -h -t {SESSION}:0")   # -h 水平分割（左右），目标窗格 0.0
    for _ in range(3):   # 再垂直分割3次，制造 2x2 效果
        run(f"tmux split-window -v -t {SESSION}:0")  # -v 垂直分割（上下）
    run(f"tmux select-layout -t {SESSION}:0 tiled")   # 自动平铺排列

    # 【重点11】enumerate 同时拿索引和元素，idx 对应窗格编号 0.0, 0.1...
    for idx, (name, cmd) in enumerate(JOBS):
        log = LOG_DIR / f"{name}.log"  # Path / str = Path
        
        # 【重点12】管道重定向：2>&1 标准错误转标准输出，tee 既显示又存文件
        # 注意：整个 cmd 用双引号包，所以 cmd 内部不能有未转义的双引号
        run(f'tmux send-keys -t {SESSION}:0.{idx} "{cmd} 2>&1 | tee {log}" C-m')
        
        time.sleep(1.5)  # 错开启动，避免同时抢资源

    print("📌 启动完成！日志目录：", LOG_DIR)
    print("   ./start_demo.py -k  可彻底关闭")
    
    # 【重点13】try-except 捕获 Ctrl+C，优雅退出
    try:
        run(f"tmux attach-session -t {SESSION}")
    except KeyboardInterrupt:
        print("\n🛑 收到 Ctrl-C，自动清理 session …")
        kill_session()

if __name__ == "__main__":
    main()