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
sensor.set_auto_gain(True)
sensor.set_auto_whitebal(True) #
#sensor.set_pixformat(sensor.GRAYSCALE)
sensor.skip_frames(time = 2000)
clock = time.clock()

#threshold2 = [(79, 100, -128, 127, -128, 127)]
#threshold2 = [(89, 100, -128, 127, -128, 127)] #(89, 100, -17, 6, -9, 23)
threshold2 = [(63, 100, -128, 127, -127, 127)]
threshold_index = 0
blob_t = 0

while(True):
    #time.sleep(0.5)
    clock.tick()
    #img = sensor.snapshot().lens_corr(1.8)
    #img = sensor.snapshot().lens_corr(0.5)
    img = sensor.snapshot()
    blobs = img.find_blobs([threshold2[threshold_index]], pixels_threshold=1000, area_threshold=1000, merge=True)
    blob_count = 0
    for blob in blobs:
        blob_t = 1
        blob_count = blob_count + 1
        #img.draw_rectangle(blob.rect(),color=(0,255,0))
        pass
    #print(blobs[1])

    temp_data = img.find_rects(threshold = 1000)
    for r in temp_data:
        size = r.magnitude() #矩形大小
        #img.draw_rectangle(blob.rect(),color=(0,255,0))
        #img.draw_cross(blob.cx(), blob.cy(),color=(255,0,0))

        if(10000 > size > 5000)and(blob_t == 1):
            img.draw_rectangle(blob.rect(),color=(0,255,0))
            img.draw_cross(blob.cx(), blob.cy(),color=(255,0,0))
            send_frame(blob.cx(), blob.cy(), 1)
            deltax = blob.cx() - 160
            deltay = blob.cy() - 120
            dis = math.sqrt(deltax*deltax + deltay*deltay)
            print(blob.cx(),blob.cy(),dis,size)




