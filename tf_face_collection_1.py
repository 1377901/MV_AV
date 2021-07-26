import sensor, image, time,pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

largest_face = None
largest_face_timeout = 50
RED_LED_PIN = 1
BLUE_LED_PIN = 3
n = 10 #设置每个人拍摄图片数量。

#连续拍摄n张照片，每间隔3s拍摄一次。
while(n):
    clock.tick()
    #红灯亮
    pyb.LED(RED_LED_PIN).on()
    print(n)

    faces = sensor.snapshot().gamma_corr(contrast=1.5).find_features(image.HaarCascade("frontalface"))

    if faces:
        largest_face = max(faces, key = lambda f: f[2] * f[3])
        largest_face_timeout -= 1
        

    if largest_face_timeout > 10:
        face_img = sensor.get_fb().crop(roi=largest_face)
        if largest_face_timeout < 20:
            face_img.save("./original/%s.bmp" % (n) )
            n -= 1
            sensor.skip_frames(time = 3000) # Give the user time to get ready.等待3s，准备一下表情。
            #红灯灭，蓝灯亮
            pyb.LED(RED_LED_PIN).off()
            pyb.LED(BLUE_LED_PIN).on()
            largest_face_timeout = 50
    
    pyb.LED(BLUE_LED_PIN).off()
    print("Done! Reset the camera to see the saved image.")
    print(clock.fps())

