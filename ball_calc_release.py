import numpy as np
from matplotlib import pyplot as plt

calc_leap = 1
# ms
weight = 0.25
# gram
diameter = 6
# mm
start_alt = 1.5
end_alt = 0
# meter
speed = 70
# m/s
temperature = 0
# celsius
pressure = 1013.25
# hPa
angle = 0
# degree
dragco = 0.5
g = 9.8

plt.title("weight=%.2f,diameter=%.2f,speed=%.2f,angle=%.2f" % (weight, diameter, speed, angle))

airde = pressure * 100 / (287.05 * (temperature + 273.15))
sect = diameter / 2 / 1000 * diameter / 2 / 1000 * np.pi
calc_leap = calc_leap / 1000
weight = weight / 1000
x_speed = np.cos(angle * np.pi / 180) * speed
y_speed = np.sin(angle * np.pi / 180) * speed
track = np.array([[0], [start_alt], [x_speed], [y_speed]])


def drag(speed):
    drag_force = airde * speed * speed * sect * dragco / 2
    return drag_force


def move(speed, acc):
    pos_move = speed * calc_leap + acc / 2 * calc_leap * calc_leap
    end_speed = speed + acc * calc_leap
    return pos_move, end_speed


calc_count = 0

while track[1, calc_count] > end_alt:
    drag_speed = np.sqrt(np.square(track[2, calc_count]) + np.square(track[3, calc_count]))
    drag_force = drag(drag_speed)
    angle_calc = np.arctan(track[3, calc_count] / track[2, calc_count])
    x_acc = np.cos(angle_calc) * drag_force / weight
    y_acc = np.sin(angle_calc) * drag_force / weight
    if track[2, calc_count] >= 0:
        x_calc_leap = move(track[2, calc_count], -x_acc)
    else:
        x_calc_leap = move(track[2, calc_count], x_acc)
    x_move_leap = track[0, calc_count] + x_calc_leap[0]
    x_speed_leap = x_calc_leap[1]
    if track[3, calc_count] >= 0:
        y_calc_leap = move(track[3, calc_count], -y_acc - g)
    else:
        y_calc_leap = move(track[3, calc_count], y_acc - g)
    y_move_leap = track[1, calc_count] + y_calc_leap[0]
    y_speed_leap = y_calc_leap[1]
    track = np.append(track, [[x_move_leap], [y_move_leap], [x_speed_leap], [y_speed_leap]], axis=1)
    print(track[0, calc_count], track[1, calc_count], track[2, calc_count], track[3, calc_count])
    calc_count += 1

x_label = track[0]
y_label = track[1]
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.axis("equal")
plt.grid()
plt.plot(x_label, y_label)
plt.show()
