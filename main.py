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
#sensor.set_auto_gain(False) # must be turned off for color tracking
#sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

sensor.set_auto_gain(True)
sensor.set_auto_whitebal(True) #
#sensor.set_pixformat(sensor.GRAYSCALE)

#threshold2 = [(79, 100, -128, 127, -128, 127)]
#threshold2 = [(89, 100, -128, 127, -128, 127)] #(89, 100, -17, 6, -9, 23)
threshold2 = [(98, 100, -128, 127, -127, 127)]
threshold_index = 0
blob_t = 0

while(True):
    #time.sleep(0.5)
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    #img = sensor.snapshot().lens_corr(0.5)
    #img = sensor.snapshot()
    for blob in img.find_blobs([threshold2[threshold_index]], pixels_threshold=100, area_threshold=100, merge=True):
        blob_t = 1
        pass

    for r in img.find_rects(threshold = 10000):
        size = r.magnitude() #矩形大小

        if(50000 > size > 10000)and(blob_t == 1):
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy(),color=(255,0,0))
            if(blob.cx() > 0):
                send_frame(blob.cx(), blob.cy(), 1)
                print(blob.cx(),blob.cy())




