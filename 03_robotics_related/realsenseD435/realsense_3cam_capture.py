#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
精简版相机采集脚本 - 仅保留RealSense相机采集核心逻辑
用法：python3 camera_collector.py [--camera_params]
"""

import os
import time
import numpy as np
import argparse
import cv2
import pyrealsense2 as rs

class CameraCollector:
    def __init__(self, args):
        self.args = args
        self.stop_flag = False
        self.init_cameras()

    def init_cameras(self):
        """初始化RealSense相机"""
        print(">>> 初始化RealSense相机...")

        # 初始化三个相机管道
        self.pipeline_left = rs.pipeline()
        self.pipeline_right = rs.pipeline()
        self.pipeline_front = rs.pipeline()

        self.config_left = rs.config()
        self.config_right = rs.config()
        self.config_front = rs.config()

        # 通过序列号启用设备
        self.config_left.enable_device(self.args.camera_left_serial)
        self.config_right.enable_device(self.args.camera_right_serial)
        self.config_front.enable_device(self.args.camera_front_serial)

        # 配置相机流
        width, height, fps = self.args.camera_width, self.args.camera_height, 60
        for config in [self.config_left, self.config_right, self.config_front]:
            config.enable_stream(rs.stream.color, width, height, rs.format.rgb8, fps)

        # 启动相机
        for name, pipeline, config, serial in [
            ("左侧", self.pipeline_left, self.config_left, self.args.camera_left_serial),
            ("右侧", self.pipeline_right, self.config_right, self.args.camera_right_serial),
            ("前置", self.pipeline_front, self.config_front, self.args.camera_front_serial)
        ]:
            try:
                pipeline.start(config)
                print(f"✓ {name}相机已打开 (序列号: {serial})")
            except Exception as e:
                print(f"错误：无法打开{name}相机: {e}")
                self.cleanup_cameras()
                exit(1)

        # 预热相机
        print(">>> 相机预热中...")
        for _ in range(30):
            try:
                self.pipeline_left.wait_for_frames(timeout_ms=1000)
                self.pipeline_right.wait_for_frames(timeout_ms=1000)
                self.pipeline_front.wait_for_frames(timeout_ms=1000)
            except:
                pass
        print("✓ 相机预热完成")

        # 初始化第一帧
        print(">>> 初始化相机第一帧...")
        for _ in range(10):
            self.read_cameras_nonblocking()
            if all([self.latest_img_left, self.latest_img_right, self.latest_img_front]):
                print("✓ 相机第一帧就绪")
                break
            time.sleep(0.1)

        if not all([self.latest_img_left, self.latest_img_right, self.latest_img_front]):
            print("警告：部分相机未能获取第一帧")
            self.cleanup_cameras()
            exit(1)

    def read_cameras_nonblocking(self):
        """非阻塞读取三个相机帧"""
        try:
            frames_left = self.pipeline_left.poll_for_frames()
            frames_right = self.pipeline_right.poll_for_frames()
            frames_front = self.pipeline_front.poll_for_frames()

            if frames_left:
                if color_frame := frames_left.get_color_frame():
                    self.latest_img_left = np.asanyarray(color_frame.get_data())

            if frames_right:
                if color_frame := frames_right.get_color_frame():
                    self.latest_img_right = np.asanyarray(color_frame.get_data())

            if frames_front:
                if color_frame := frames_front.get_color_frame():
                    self.latest_img_front = np.asanyarray(color_frame.get_data())

        except Exception:
            pass

    def get_frame(self):
        """获取当前缓存的图像帧"""
        try:
            if not all([self.latest_img_left, self.latest_img_right, self.latest_img_front]):
                print("警告：部分图像数据不可用")
                return False

            return (self.latest_img_front.copy(),
                    self.latest_img_left.copy(), 
                    self.latest_img_right.copy())
        except Exception as e:
            print(f"获取帧异常: {e}")
            return False

    def process(self):
        """主采集循环"""
        print(f">>> 采集已启动 (目标帧数: {self.args.max_timesteps})")

        frame_interval = 1.0 / self.args.frame_rate
        count = 0

        try:
            while count < self.args.max_timesteps and not self.stop_flag:
                loop_start = time.time()

                # 采集当前帧
                self.read_cameras_nonblocking()
                if not (result := self.get_frame()):
                    time.sleep(frame_interval)
                    continue

                img_front, img_left, img_right = result

                # 显示图像
                display_front = cv2.cvtColor(img_front, cv2.COLOR_RGB2BGR)
                display_left = cv2.cvtColor(img_left, cv2.COLOR_RGB2BGR)
                display_right = cv2.cvtColor(img_right, cv2.COLOR_RGB2BGR)

                combined = np.hstack((display_left, display_front, display_right))
                h, w, _ = combined.shape
                resized = cv2.resize(combined, (1280, int(1280/w*h)))
                cv2.imshow('Camera Views (Left | Front | Right)', resized)

                # 按键检测
                if (key := cv2.waitKey(1) & 0xFF) in [ord('q'), ord(' ')]:
                    print(">>> 采集被用户中断")
                    self.stop_flag = True

                count += 1
                if count % 50 == 0 or count <= 5:
                    print(f"已采集: {count}/{self.args.max_timesteps} 帧")

                # 帧率控制
                elapsed = time.time() - loop_start
                if (sleep_time := frame_interval - elapsed) > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            print(">>> 采集被用户中断")

        print(f">>> 采集结束，共 {count} 帧")
        return count

    def cleanup_cameras(self):
        """释放相机资源"""
        print(">>> 释放RealSense相机资源...")
        for name, pipeline in [("左侧", self.pipeline_left), 
                               ("右侧", self.pipeline_right), 
                               ("前置", self.pipeline_front)]:
            try:
                pipeline.stop()
                print(f"✓ {name}相机已释放")
            except Exception as e:
                print(f"警告：释放{name}相机时出错: {e}")
        print("✓ 相机资源释放完成")

def get_arguments():
    parser = argparse.ArgumentParser()
    # 相机序列号
    parser.add_argument('--camera_front_serial', type=str, default='152122074605')
    parser.add_argument('--camera_left_serial', type=str, default='152222071100')
    parser.add_argument('--camera_right_serial', type=str, default='151222076708')
    # 相机参数
    parser.add_argument('--camera_width', type=int, default=640)
    parser.add_argument('--camera_height', type=int, default=480)
    parser.add_argument('--frame_rate', type=int, default=30)
    # 采集参数
    parser.add_argument('--max_timesteps', type=int, default=500)
    return parser.parse_args()

def main():
    args = get_arguments()
    collector = CameraCollector(args)

    try:
        collector.process()
    finally:
        collector.cleanup_cameras()
        cv2.destroyAllWindows()
        cv2.waitKey(1)
        print("✓ 程序正常退出")

if __name__ == '__main__':
    main()
