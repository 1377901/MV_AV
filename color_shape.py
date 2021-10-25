import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# thresholds = [(0, 0, -1, 2, -1, 1)]
black = [(0, 0, -1, 2, -1, 1)]
white = [(80, 100, -1, 100, -1, 100)]

while(True):
    #time.sleep(0.5)
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    for r in img.find_rects(threshold = 10000):
    # for r in img.find_rects(thresholds):

        area = r.rect()
        #print(r.w(),r.h())
        size = r.magnitude() #矩形大小
        if(20000 < size < 50000):
            img.draw_rectangle(r.rect(), color = (255, 0, 0))
            print(r.w(),r.h())
        #print(size)
            for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))

        statistics = img.get_statistics(roi=area)#像素颜色统计
        #if 80<statistics.l_mode()<100 and -1<statistics.a_mode()<1 and -1<statistics.b_mode()<1:
            #for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))

        # print(r)
    #black_blobs = img.find_blobs(white)
    ##black_blobs = img.find_blobs(10000)
    #for b in black_blobs:
        #print(b.cx())
        #img.draw_rectangle(b.rect(), color = (0, 0, 255))
        #print(b.w(),b.h())


    #print("FPS %f" % clock.fps())
