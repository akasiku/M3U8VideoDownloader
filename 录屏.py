import pyautogui
import cv2
import numpy as np

# 设置录制参数
screen_size = (1920, 1080)  # 屏幕分辨率
output_filename = "录屏文件.mp4"
fps = 30.0  # 每秒帧数

# 开始录制
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)
print("开始录屏,结束录屏返回这个界面,并按Ctr+c")
while True:
    # 获取屏幕截图并写入视频
    img = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    out.write(frame)
    # 按下键盘上的 'q' 键停止录制
    if cv2.waitKey(1) == ord("q"):
        break
# 清理并释放资源
out.release()
cv2.destroyAllWindows()