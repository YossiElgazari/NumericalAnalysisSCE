'''
 produces line by the least square method from a given set of xy-coordinates
'''

#TODO - install matplotlib package to fully enjoy the program.
import matplotlib.pyplot as plt
import sys


def location(c, scale):
    temp = c
    prev = 0
    while temp >= 10 * scale:
        temp = temp - 10 * scale
    prev = c - temp
    line = temp / scale
    return prev, int(round(line))


class Point:
    # scale in units/mm
    x_scale = 0.1
    y_scale = 0.1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_prev, self.x_line = location(x, self.x_scale)
        self.y_prev, self.y_line = location(y, self.y_scale)

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    @classmethod
    def set_scales(cls, x_scale_in, y_scale_in):
        cls.x_scale = x_scale_in
        cls.y_scale = y_scale_in


class Pointset:
    def __init__(self, point_list):
        self.str_point_list = point_list
        self.n = len(point_list)
        self.point_list = []
        self.x_list = []
        self.y_list = []
        for element in point_list:
            temp_element = point_parse(element)
            self.point_list.append(temp_element)

        for point in self.point_list:
            self.x_list.append(point.x)
            self.y_list.append(point.y)

    def __str__(self):
        return str(self.str_point_list)

    def __repr__(self):
        return str(self.str_point_list)

    @property
    def points_mean(self):
        tot_x = 0
        tot_y = 0
        for temp_point in self.point_list:
            tot_x += temp_point.x
            tot_y += temp_point.y

        return Point(tot_x / len(self.point_list), tot_y / len(self.point_list))

    @property
    def sum_squared(self):
        tot = 0
        for temp_point in self.point_list:
            tot += temp_point.x * temp_point.x

        return tot

    @property
    def sum_prod(self):
        tot = 0
        for temp_point in self.point_list:
            tot += temp_point.x * temp_point.y
        return tot

    @property
    def calc_m(self):
        return (self.sum_prod - self.n * self.points_mean.x * self.points_mean.y) / (
                self.sum_squared - self.n * self.points_mean.x * self.points_mean.x)

    @property
    def calc_c(self):
        return (self.points_mean.y * self.sum_squared - self.points_mean.x * self.sum_prod) / (
                self.sum_squared - self.n * self.points_mean.x * self.points_mean.x)

    @property
    def y_new_list(self):
        new_list = []
        for x in self.x_list:
            new_list.append(x * self.calc_m + self.calc_c)

        return new_list


# (x,y)


def point_parse(a):
    temp = a
    temp = temp[1:-1]
    temp_x, temp_y = temp.split(',')
    try:
        return Point(int(temp_x), int(temp_y))
    except ValueError:
        return Point(float(temp_x), float(temp_y))


def main():
    a = sys.argv[1:]
    temp_points = []
    p = [[0, 1], [3, 2], [5, 8]]
    for i in range(len(p)):
        temp_x, temp_y = p[i][0], p[i][1]
        temp_points.append(('({},{})'.format(temp_x, temp_y)))
    points = Pointset(temp_points)
    line = 'y = ({}) x + ({})'.format(round(points.calc_m, 3), round(points.calc_c, 3))
    plt.plot(points.x_list, points.y_new_list, label=line, color='red', alpha=0.5)
    plt.scatter(points.x_list, points.y_new_list, s=50, color='red', alpha=0.8)
    plt.scatter(points.x_list, points.y_list, s=50, alpha=0.5)

    for i in points.point_list:
        plt.annotate([i.x, i.y], (i.x, i.y), color='b', horizontalalignment='right', verticalalignment='baseline',
                     fontsize=8, rotation=0)

    new_list = list(zip(points.x_list, points.y_new_list))
    for point in new_list:
        plt.annotate([round(point[0], 3), round(point[1], 3)], (point[0], point[1]), color='r',
                     horizontalalignment='left', verticalalignment='top', fontsize=8, rotation=0)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
