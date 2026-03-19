realsense相机配置

1. 安装 ROS Noetic 版本的 RealSense 相机驱动包
sudo apt-get install ros-noetic-realsense2-camera

2. 硬件realsense相机id序列号（例如：213322070316）在底部

3. 找realsense相机功能包下载的位置
rospack find realsense2_camera

4. mv移动的文件以上一步find的路径为准
cd ~/cobot_magic/camera_ws/src/realsense-ros/realsense2_camera/launch && sudo mv multi_camera.launch /opt/ros/noetic/share/realsense2_camera/launch/

5. 修改multi_camera.launch文件相机id配置
vim /opt/ros/noetic/share/realsense2_camera/launch/multi_camera.launch

6. 查看硬件是否正确识别，验证相机是否成功启动
lsusb
roslaunch realsense2_camera rs_camera.launch