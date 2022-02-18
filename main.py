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
threshold2 = [(81, 100, -128, 127, -127, 127)]
threshold_index = 0


while(True):
    blob_flag = 0
    rect_flag = 0
    clock.tick()
    img = sensor.snapshot()
    blobs = img.find_blobs([threshold2[threshold_index]], pixels_threshold=500, area_threshold=500, merge=True)
    temp_data = img.find_rects(threshold = 100)
    blob_count = 0
    blob_area = 0
    blob_area1 = 0

    rect_count = 0
    rect_area = 0
    rect_area1 = 0

    for blob in blobs:
        blob_flag = 1
        blob_count = blob_count + 1
        blob_area = blob_area + blob.w()*blob.h()
    if(blob_flag == 1):blob_area1 = blob_area / blob_count

    for r in temp_data:
        rect_flag = 1
        rect_count = rect_count + 1
        rect_area = rect_area + r.magnitude()
    if(rect_flag == 1):rect_area1 = rect_area / rect_count

    if(rect_flag == 1)and(blob_flag == 1):
        print(blob_area1,rect_area1)

    for blob in blobs:
        blob_area_frame = blob.w()*blob.h()
        #if(rect_flag == 1)and(blob_flag == 1):
        if(rect_flag == 1)and(blob_flag == 1)and(blob_area1* 1.8 >= blob_area_frame >= 0.5*blob_area1)and(blob_area1 < 20000): #and(blob_area <= rect_area1)
            img.draw_rectangle(blob.rect(),color=(0,255,0))
            img.draw_cross(blob.cx(), blob.cy(),color=(255,0,0))
            send_frame(blob.cx(), blob.cy(), 1)
            deltax = blob.cx() - 160
            deltay = blob.cy() - 120
            dis = math.sqrt(deltax*deltax + deltay*deltay)
            print(blob.cx(),blob.cy(),dis,blob_area_frame)




