'''
 produces line by the least square method from a given set of xy-coordinates
'''

# TODO - install matplotlib package to fully enjoy the program.
import matplotlib.pyplot as plt
import sys
from Interpolation import print_matrix
from gaussElimination import gaussElimination


def location(c, scale):
    """

    :param c: x value of a point
    :param scale: Int, 0.1
    :return: Tuple
    """
    temp = c
    prev = 0
    # As long as temp is bigger than 1
    while temp >= 10 * scale:
        # subtract 1 from temp
        temp = temp - 10 * scale
    # End of while loop -> temp is a number between 0 and 1
    prev = c - temp
    line = temp / scale
    return prev, int(round(line))


class Point:
    """
    Class Point, represents a point in a 2D dimension.
    """
    # scale in units/mm
    x_scale = 0.1
    y_scale = 0.1

    def __init__(self, x, y):
        """
        Ctor, class Point
        :param x: the x value of the point
        :param y: the y value of the point
        """
        self.x = x
        self.y = y
        self.x_prev, self.x_line = location(x, self.x_scale)
        self.y_prev, self.y_line = location(y, self.y_scale)

    def __str__(self):
        """

        :return: String representation of  a point i.e: (1,2)
        """
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    @classmethod
    def set_scales(cls, x_scale_in, y_scale_in):
        """
        sets y scale and x scale
        :param x_scale_in: new x scale
        :param y_scale_in: new y scale
        """
        cls.x_scale = x_scale_in
        cls.y_scale = y_scale_in


class Pointset:
    """
    Class Pointset, handles a set of points
    Holds:
     - array of the points as strings
     - the number of points its holds
     - list of Points (class)
     - list of x values
     - list of y values (so Xi and Yi are the point in index i)
    """

    def __init__(self, point_list):
        """
        Ctor

        :param point_list: A list containing strings, each represents a point in this format:(0,1)
        """
        self.str_point_list = point_list
        self.n = len(point_list)
        self.point_list = []
        self.x_list = []
        self.y_list = []
        # For every string that represents a point
        for element in point_list:
            # Convert it to a Point(object)
            temp_element = point_parse(element)
            # Add it to the point list
            self.point_list.append(temp_element)
        # For every point in the Points list
        for point in self.point_list:
            # Add it's x value to the x list
            self.x_list.append(point.x)
            # Add it's y value to the y list
            self.y_list.append(point.y)

    def __str__(self):
        """

        :return: String representation of the object, i.e: [(1,2), (3,4), ...]
        """
        return str(self.str_point_list)

    def __repr__(self):
        return str(self.str_point_list)

    @property
    def points_mean(self):
        """

        :return: Point (x,y), x is the average value of all the X's in the points list, same goes for y.
        """
        tot_x = 0
        tot_y = 0
        # for every Point in the points list
        for temp_point in self.point_list:
            # sum it's x value
            tot_x += temp_point.x
            # sum it's y value
            tot_y += temp_point.y
        # Point(x_average, y_average)
        return Point(tot_x / len(self.point_list), tot_y / len(self.point_list))

    @property
    def sum_squared(self):
        """

        :return: Float, representing the sum of x^2 for every x value in the points list
        """
        tot = 0
        for temp_point in self.point_list:
            tot += temp_point.x * temp_point.x

        return tot

    @property
    def sum_prod(self):
        """

        :return: Float, representing the sum of x*y for every point in the points list
        """
        tot = 0
        for temp_point in self.point_list:
            tot += temp_point.x * temp_point.y
        return tot

    @property
    def calc_m(self):
        """

        :return: Float, The incline of the final line(the m of : y = m*x + c)
        """
        # ( sum(Xi * Yi) - (size * x_average * y_average) ) / ( sum(Xi^2) - (size * x_average * x_average) )
        return (self.sum_prod - self.n * self.points_mean.x * self.points_mean.y) / (
                self.sum_squared - self.n * self.points_mean.x * self.points_mean.x)

    @property
    def calc_c(self):
        """

        :return: Float, The intersection with the y-axis of the final line(the c of : y = m*x + c)
        """
        # ( (y_average * sum(Xi^2)) - (x_average * sum(Xi * Yi)) ) / ( sum(Xi^2) - (size * x_average * x_average) )
        return (self.points_mean.y * self.sum_squared - self.points_mean.x * self.sum_prod) / (
                self.sum_squared - self.n * self.points_mean.x * self.points_mean.x)

    @property
    def y_new_list(self):
        """

        :return: List, containing all the new y values for all the x values in the x list, so the best line will
        go through those points.
        """

        new_list = []
        # For every x in the x list
        for x in self.x_list:
            # calculate it's new matching y based of the best line equation (y = m*x + c)
            new_list.append(x * self.calc_m + self.calc_c)

        return new_list


# (x,y)


def point_parse(a):
    """
    Gets a point as a string '(1,2)' and converts it to a Point(object)

    :param a: the string representing a point to parse.
    :return: Point object,
    """
    temp = a
    # remove the parenthesis from the string.
    temp = temp[1:-1]
    # takes the numerical x and y values
    temp_x, temp_y = temp.split(',')
    try:
        # if they are Int values
        return Point(int(temp_x), int(temp_y))
    except ValueError:
        # else, return them as a float
        return Point(float(temp_x), float(temp_y))


def printMatrix(point_set: Pointset):
    a11 = point_set.sum_squared
    a12 = sum(point_set.x_list)
    a21 = a12
    a22 = point_set.n
    sol1 = point_set.sum_prod
    sol2 = sum(point_set.y_list)
    matrix = [[a11, a12, sol1], [a21, a22, sol2]]
    print_matrix(matrix)
    print_matrix(gaussElimination(matrix))


def main():
    a = sys.argv[1:]
    # List that store all the points we ran on so far in thw while loop
    temp_points = []
    # TODO - Replace p data for another solution as you wish, [[x1,y1],[x2,y2],...,[xn,yn]]
    p = [[0, 1], [3, 2], [5, 8]]
    # For every point in the input array
    for i in range(len(p)):
        # Extract it's x anf y
        temp_x, temp_y = p[i][0], p[i][1]
        # Add the point to the list
        temp_points.append(('({},{})'.format(temp_x, temp_y)))
    # Initialize a PointSet with the temp points
    points = Pointset(temp_points)
    printMatrix(point_set=points)
    # Initialize the best line fit corresponding to the point set, y = m*x +n
    line = 'y = ({}) x + ({})'.format(round(points.calc_m, 3), round(points.calc_c, 3))
    # Visualize the results
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
