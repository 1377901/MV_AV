import sensor, image, time, pyb, math

##配置输出
uart_baudrate = 115200
uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)
def send_frame(cx, cy, flag):
     uart.writechar(0xA5)
     uart.writechar(0x5A)
     uart.writechar(cx)
     uart.writechar(cy)
     uart.writechar(cx + cy) #校验位
     uart.writechar(flag)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

#threshold2 = [(79, 100, -128, 127, -128, 127)]
threshold2 = [(89, 100, -128, 127, -128, 127)]
threshold_index = 0

while(True):
    #time.sleep(0.5)
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    for blob in img.find_blobs([threshold2[threshold_index]], pixels_threshold=100, area_threshold=100, merge=True):
        pass

    for r in img.find_rects(threshold = 10000):
        size = r.magnitude() #矩形大小
        temp_cx = 0
        temp_cy = 0
        if(30000 > size > 10000):
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())
            for p in r.corners():
                #img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
                temp_cx = temp_cx + p[0]
                temp_cy = temp_cy + p[1]
            if (temp_cx > 0):
                tx = (int)(temp_cx / 4)
                ty = (int)(temp_cy / 4)
                # send_frame(tx, ty, 1)
                # print(tx,ty)
            if(blob.cx() > 0):
                send_frame(blob.cx(), blob.cy(), 1)
                print(blob.cx(),blob.cy()) 




