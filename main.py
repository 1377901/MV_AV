import image, math, pyb, sensor, struct, time

##配置输出
uart_baudrate = 115200
uart = pyb.UART(3, uart_baudrate, timeout_char = 1000)
def send_frame(cx, cy, flag, time, lat, lon):
     uart.writechar(0xA5)
     uart.writechar(0x5A)
     uart.writechar(cx)
     uart.writechar(cy)
     uart.writechar(cx + cy) #校验位
     uart.writechar(flag)
     uart.writechar(time)
     uart.writechar(lat)
     uart.writechar(lon)

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
temp_data= 135  #Tag码边长
valid_tag_ids = {
            0 : temp_data,
            1 : temp_data,
            2 : temp_data,
        }

##镜头参数
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

##功能函数
clock = time.clock()
tag_flag = 0  ##指定该点位的有效性 0:表示无效 1：表示有效
loiter_time = 0 ##指定无人机在TAG处悬停时间
position_lat = None
position_lon = None

while(True):
    clock.tick()
    img = sensor.snapshot()
    tags = sorted(img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y), key = lambda x: x.w() * x.h(), reverse = True)
    if tags and (tags[0].id() in valid_tag_ids):
        img.draw_rectangle(tags[0].rect())
        img.draw_cross(tags[0].cx(), tags[0].cy(), color = (0, 255, 0), size=10)
        if tags.id() == 0: ##TAG 0 代表降落点--禁止修改
            tag_flag = 1
            loiter_time = 0
            position_lat = 0
            position_lon = 0
            send_frame(tags[0].cx(), tags[0].cy(), tag_flag, loiter_time, position_lat, position_lon)
        if tags.id() == 1: ##假设TAG 1 代表香蕉
            tag_flag = 1 #启用该点
            loiter_time = 5 ##指定该点的悬停时间--秒
            position_lat = None ##指定该TAG投放点的纬度
            position_lon = None ##指定该TAG投放点的经度
            send_frame(tags[0].cx(), tags[0].cy(), tag_flag, loiter_time, position_lat, position_lon)
        if tags.id() == 2: ##假设TAG 2 代表苹果
            tag_flag = 1 #启用该点
            loiter_time = 5 ##指定该点的悬停时间--秒
            position_lat = None ##指定该TAG投放点的纬度
            position_lon = None ##指定该TAG投放点的经度
            send_frame(tags[0].cx(), tags[0].cy(), tag_flag, loiter_time, position_lat, position_lon)
        if tags.id() == 3: ##假设TAG 3 代表橘子
            tag_flag = 1 #启用该点
            loiter_time = 5 ##指定该点的悬停时间--秒
            position_lat = None ##指定该TAG投放点的纬度
            position_lon = None ##指定该TAG投放点的经度
            send_frame(tags[0].cx(), tags[0].cy(), tag_flag, loiter_time, position_lat, position_lon)

    img = 0
    tags = 0
