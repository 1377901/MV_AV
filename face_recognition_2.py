
import sensor, time, image, pyb

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.B128X128) # or sensor.QQVGA (or others)
sensor.set_windowing((92,112))
sensor.skip_frames(10) # Let new settings take affect.
sensor.skip_frames(time = 5000) #等待5s

uart_baudrate = 115200
uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)

# 自定义帧发送函数
def send_frame(cx, cy):
     uart.writechar(0xA5)
     uart.writechar(0x5A)
     uart.writechar(cx)
     uart.writechar(cy)
     uart.writechar(cx + cy)


img = image.Image("../original/1.bmp").mask_ellipse() #目标图像所在目录
d0 = img.find_lbp((0, 0, img.width(), img.height()))  #d0为当前人脸的lbp特征
img = None
face_cascade = image.HaarCascade("frontalface", stages=25)


print("")
clock = time.clock()
while(True):
    clock.tick()
    # img = sensor.snapshot()
    img = sensor.snapshot().gamma_corr(contrast=1.5) #拍摄当前图像
    dist = 0
    d1 = img.find_lbp((0, 0, img.width(), img.height()))
    dist = image.match_descriptor(d0, d1) #计算d0 d1即样本图像与被检测人脸的特征差异度。
    if (dist < 100): #识别到目标
        objects = img.find_features(face_cascade, threshold=0.95, scale_factor=1.25)
        # Draw objects
        for r in objects:
            img.draw_rectangle(r, color = (255, 0, 0))
            img.draw_cross(r.cx(), r.cy(), color = (0, 255, 0))
            send_frame(r.cx(), r.cy())
            print("Object x:%d: y:%d, The dis: %f"%(r.cx(), r.cy(),dist))

    #print(clock.fps())







