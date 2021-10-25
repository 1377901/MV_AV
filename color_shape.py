import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

while(True):
    #time.sleep(0.5)
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    for r in img.find_rects(threshold = 10000):

        area = r.rect()
        size = r.magnitude() #矩形大小
        if(15000 < size < 25000):
            img.draw_rectangle(r.rect(), color = (255, 0, 0))
            print(r.w(),r.h())
        if(size > 25000):
            for p in r.corners():
                img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))




