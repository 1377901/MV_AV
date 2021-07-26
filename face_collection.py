
import sensor, image, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3
SUB = "original"  #目标图像所在目录

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.B128X128) # or sensor.QQVGA (or others)
sensor.set_windowing((92,112))
sensor.skip_frames(10) # Let new settings take affect.
sensor.skip_frames(time = 2000)

n = 10 #设置每个人拍摄图片数量。

#连续拍摄n张照片，每间隔3s拍摄一次。
while(n):
    #红灯亮
    pyb.LED(RED_LED_PIN).on()
    sensor.skip_frames(time = 3000) # Give the user time to get ready.等待3s，准备一下表情。

    #红灯灭，蓝灯亮
    pyb.LED(RED_LED_PIN).off()
    pyb.LED(BLUE_LED_PIN).on()

    #保存截取到的图片到SD卡
    print(n)
    sensor.snapshot().save("./original/%s.pgm" % (n) )

    n -= 1

    pyb.LED(BLUE_LED_PIN).off()
    print("Done! Reset the camera to see the saved image.")
    #sensor.reset()
