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

print(np.finfo(np.longdouble))
plt.title("weight=%.2f,diameter=%.2f,speed=%.2f,angle=%.2f" % (weight, diameter, speed, angle))

airde = np.divide(np.multiply(pressure, 100), np.multiply(287.05, np.add(temperature, 273.15)))
sect = np.multiply(np.divide(np.power(diameter, 2), 4000000), np.pi)
calc_leap = np.divide(calc_leap, 1000)
weight = np.divide(weight, 1000)
angle_rad = np.deg2rad(angle)
x_speed = np.multiply(np.cos(angle_rad), speed)
y_speed = np.multiply(np.sin(angle_rad), speed)
track = np.array([[0], [start_alt], [x_speed], [y_speed]])
track.astype("longdouble")


def drag(speed):
    drag_force = np.divide(np.multiply(np.multiply(airde, np.power(speed, 2)), np.multiply(sect, dragco)), 2)
    return drag_force


def move(speed, acc):
    pos_move = np.add(np.multiply(speed, calc_leap), np.multiply(np.divide(acc, 2), np.power(calc_leap, 2)))
    end_speed = np.add(speed, np.multiply(acc, calc_leap))
    return pos_move, end_speed


calc_count = 0

while track[1, calc_count] > end_alt:
    drag_speed = np.sqrt(np.add(np.square(track[2, calc_count]), np.square(track[3, calc_count])))
    drag_force = drag(drag_speed)
    angle_calc = np.arctan(np.divide(track[3, calc_count], track[2, calc_count]))
    acc = np.divide(drag_force, weight)
    x_acc = np.multiply(np.cos(angle_calc), acc)
    y_acc = np.multiply(np.sin(angle_calc), acc)
    if track[2, calc_count] >= 0:
        x_calc_leap = move(track[2, calc_count], -x_acc)
    else:
        x_calc_leap = move(track[2, calc_count], x_acc)
    x_move_leap = np.add(track[0, calc_count], x_calc_leap[0])
    x_speed_leap = x_calc_leap[1]
    if track[3, calc_count] >= 0:
        y_calc_leap = move(track[3, calc_count], np.subtract(-y_acc, g))
    else:
        y_calc_leap = move(track[3, calc_count], np.subtract(y_acc, g))
    y_move_leap = np.add(track[1, calc_count], y_calc_leap[0])
    y_speed_leap = y_calc_leap[1]
    track = np.append(track, [[x_move_leap], [y_move_leap], [x_speed_leap], [y_speed_leap]], axis=1)
    print(track[0, calc_count], track[1, calc_count], track[2, calc_count], track[3, calc_count])
    calc_count = np.add(calc_count, 1)

x_label = track[0]
y_label = track[1]
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.axis("equal")
plt.grid()
plt.plot(x_label, y_label)
plt.show()
