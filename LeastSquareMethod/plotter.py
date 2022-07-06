import script
import sys


def main():
    arg = sys.argv[1:]
    x_scale = float(arg[1])
    y_scale = float(arg[2])
    script.Point.set_scales(x_scale, y_scale)
    file_path = arg[0]
    pt_list = []
    with open(file_path, 'r') as f:
        for line in f:
            temp_x, temp_y = line.split(',')
            pt_list.append(('({},{})'.format(temp_x, temp_y)))

    points = script.Pointset(pt_list)
    print('On X axis 1mm = {} units\nOn Y axis 1mm = {} units\n'.format(script.Point.x_scale, script.Point.y_scale))
    for point in points.point_list:
        print(point, '\n{} lines after {} on X axis \n{} lines above {} on Y axis\n'.format(point.x_line, point.x_prev, point.y_line, point.y_prev))


main()

'''
temp_x, temp_y = line.split(',')
temp_points.append(('({},{})'.format(temp_x, temp_y)))

'''
