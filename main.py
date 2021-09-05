import image, math, pyb, sensor, struct, time
uart_baudrate = 115200
uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)
def send_frame(cx, cy):
     uart.writechar(0xA5)
     uart.writechar(0x5A)
     uart.writechar(cx)
     uart.writechar(cy)
     uart.writechar(cx + cy)
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
temp_data= 135
valid_tag_ids = {
                  0 : temp_data,
                  1 : temp_data,
                  2 : temp_data,
                }
lens_mm = 1.7
lens_to_camera_mm = 22
sensor_w_mm = 3.6736
sensor_h_mm = 2.7384
x_res = 320
y_res = 240
f_x = (lens_mm / sensor_w_mm) * x_res
f_y = (lens_mm / sensor_h_mm) * y_res
c_x = x_res / 2
c_y = y_res / 2
h_fov = 2 * math.atan((sensor_w_mm / 2) / lens_mm)
v_fov = 2 * math.atan((sensor_h_mm / 2) / lens_mm)
clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    tags = sorted(img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y), key = lambda x: x.w() * x.h(), reverse = True)
    if tags and (tags[0].id() in valid_tag_ids):
        img.draw_rectangle(tags[0].rect())
        img.draw_cross(tags[0].cx(), tags[0].cy(),color = (0, 255, 0),size=10)
        send_frame(tags[0].cx(), tags[0].cy())
    img = 0;
    tags = 0;