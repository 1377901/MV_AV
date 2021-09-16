import time, sensor, image
import image, math, pyb, struct
from image import SEARCH_EX, SEARCH_DS

##配置输出
uart_baudrate = 115200
uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)
def send_frame(cx, cy):
     uart.writechar(0xA5)
     uart.writechar(0x5A)
     uart.writechar(cx)
     uart.writechar(cy)
     uart.writechar(cx + cy) #校验位


sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.QQVGA)
#sensor.set_windowing(((640-80)//2, (480-60)//2, 80, 60))
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.skip_frames(time = 2000)


template = image.Image("/template.pgm")
#加载模板图片

clock = time.clock()

# Run template matching
while (True):
    clock.tick()
    img = sensor.snapshot()
    r = img.find_template(template, 0.70, step=4, search=SEARCH_EX) #, roi=(10, 0, 60, 60))
    #find_template(template, threshold, [roi, step, search]),threshold中的0.7是相似度阈值,roi是进行匹配的区域（左上顶点为（10，0），长80宽60的矩形），
    #注意roi的大小要比模板图片大，比frambuffer小。
    #把匹配到的图像标记出来
    if r:
        img.draw_rectangle(r)
        img.draw_cross(r.cx(), r.cy(), color = (0, 255, 0), size=10)
        send_frame(r.cx(), r.cy())

    print(clock.fps())
