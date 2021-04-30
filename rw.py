### random walking code ###

 ## walking subroutines ##

 # updates a 3d coordinate by the given delta, d  # ie. incr( (1, 1, 1), (-2, 0, 5) ) will return (-1, 1, 6)

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, o):
        return True if (self.a == o.a and self.b == o.b) or (self.a == o.b and self.b == o.a) else False

    def __ne__(self, o):
        return self != o

    def __hash__(self):
        return ((self.a.x + self.b.x) * 18397 // 2) + ((self.a.y + self.b.y) * 20483 // 2) + ((self.a.z + self.b.z) * 29303 // 2)
        #return int(f"{abs(self.x)}{abs(self.y)}{abs(self.z)}")

    def __repr__(self):
        return f"p({self.x}, {self.y}, {self.z})"

    def add(self, i, j, k):
        return point(self.x + i, self.y + j, self.z + k)

    def shift(self, i, j, k):
        self.x += i
        self.y += j
        self.z += k

class point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, o):
        return True if (self.x == o.x and self.y == o.y and self.z == o.z) else False

    def __ne__(self, o):
        return self != o

    def __hash__(self):
        return (self.x * 18397) + (self.y * 20483) + (self.z * 29303)
        #return int(f"{abs(self.x)}{abs(self.y)}{abs(self.z)}")

    def __repr__(self):
        return f"p({self.x}, {self.y}, {self.z})"

    def add(self, i, j, k):
        return point(self.x + i, self.y + j, self.z + k)

    def shift(self, i, j, k):
        self.x += i
        self.y += j
        self.z += k

def incr(p, d):
    return [p[0] + d[0], p[1] + d[1], p[2] + d[2]] # returns all the cardinal coordinates that are b units away from coordinate a

def expand(a, b):
    return [
        a.add(b, 0, 0),
        a.add(-b, 0, 0),
        a.add(0, b, 0),
        a.add(0, -b, 0),
        a.add(0, 0, b),
        a.add(0, 0, -b)
    ]
 # prints out formatted path
def print_path(p):
    s = ""
    for point in p:
        s += f"({point.x}, {point.y}, {point.z}) -> "
    print(f"Path: {s[:-4]}")

def print_path_datawise(p):
    s = ""
    for i in range(len(p)):
        s += f"({p[0][i]}, {p[1][i]}, {p[2][i]}) -> "
    print(f"Path: {s[:-4]}")

 # calculates the vector distance from the origin
def mag3D(x, y, z):
    return math.sqrt( ( x ** 2 ) + ( y ** 2 ) + ( z ** 2 ) )

 ## walking code ##

def generate_path_datawise(a, b, c, l):
    p = point(a, b, c)
    points = list()
    points.append(p)
    for i in range(l):
        options = expand(p, 1) # get options
        valid_options = list(filter(lambda e: e not in points, options))
        if len(valid_options) == 0:
            print(f"short ({len(points)})")
            return points
        import random
        n = random.choice(valid_options)
        #j = random.randint(0, len(valid_options) - 1)
        #import secrets
        #j = secrets.randbelow(len(valid_options))
        #n = valid_options[j]
        #print(f"j = {j}")
        points.append(n)
        p = n
    return points

def blob(l, path_length):
    executor = concurrent.futures.ProcessPoolExecutor(61)
    futures = [executor.submit(generate_path_datawise, l[0], l[1], l[2], path_length)
        for i in range(n_iter)]
    concurrent.futures.wait(futures)

def main(n_iter):
    #random.seed(datetime.now())
    #random.seed(83710967093847014376983476109437)

    #for i in range(50):
    #    print(secrets.randbelow(50))

    main_fig = plt.figure()
    main_ax = plt.axes(projection='3d')

    all_runs = list()
    queue = Queue()

    multi = True

    #step = 44
    #processes = [ Process(  target=generate_path_datawise, args=(path_length, queue )  ) for i in range(num_walks) ]
    #length = len(processes)
    #for i in range(0, length, step):
    #    for j in range(i, min(i + step, length) ):
    #        processes[j].start()
    #    for j in range(i, min(i + step, length) ):
    #        processes[j].join()

    labels = [[0, 0, 0]]
    max_height = 70#280#140

    # az = 9 el = 31
    # k base
    for i in range(max_height):
        labels.append([random.randint(-2, 2), 0, i])
        labels.append([random.randint(-2, 2), 0, -i])

    #max_k = max_height * 11 // 14
    for i in range(round(max_height)):
        labels.append([random.randint(-2, 2), -i // 8, i])
        labels.append([random.randint(-2, 2), -i // 8, -i])

    futures = list()
    for l in labels:
        executor = concurrent.futures.ProcessPoolExecutor(61)
        futures += [executor.submit(generate_path_datawise, l[0], l[1], l[2], random.randint(path_length // 2, path_length)) #path_length
            for i in range(n_iter)]
        concurrent.futures.wait(futures)

    #x = list()
    #y = list()
    #z = list()
    #print(futures)
    count = 0
    point_set = set()
    line_set = set()
    #print("\n\n\n Without lists \n\n\n")
    for f in futures:
        path = f.result()
        for i in range(len(path) - 1):
            line_set.add(Line(path[i], path[i+1]))
            #main_ax.plot( [path[i].x, path[i+1].x], [path[i].y, path[i+1].y], [path[i].z, path[i+1].z], color = 'g' )
        for point in path:
            #x.append(point.x)
            #y.append(point.y)
            #z.append(point.z)
            point_set.add(point)

    num_walks = n_iter

    if show_paths:
        for line in line_set:
            main_ax.plot( [line.a.x, line.b.x], [line.a.y, line.b.y], [line.a.z, line.b.z], color = 'g' )

    if show_points:
        x_set = list()
        y_set = list()
        z_set = list()
        for p in point_set:
            x_set.append(p.x)
            y_set.append(p.y)
            z_set.append(p.z)
        main_ax.scatter3D(x_set, y_set, z_set, c=z_set)

    if no_axes:
        main_ax.axis('off')

    main_ax.view_init(elev=3., azim=3.)

    #mng = plt.get_current_fig_manager()
    #mng.window.showMaximized()
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()


if __name__ == "__main__":

     ## init ##

    debug = False

    step_size = 1 # change for more paths

    n_iter = 5#10#20#400
    path_length = 145#5#20#240#65

    num_chains = 1
    percent_bond_step_length = 1.0
    bounding_number = 10000 # max distance in any direction a chain can go

    show_subplots = False

    show_paths = True

    show_points = True
    show_gyration = True

    show_gyration_on_walk_graph = False
    no_axes = True # hides axes on blob graph

     # import libraries

    import math
    from mpl_toolkits import mplot3d
    import numpy as np

    #import matplotlib
    #matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt

    from multiprocessing import Process, Queue
    import concurrent
    import concurrent.futures
    import threading

    import random
    import time
    from datetime import datetime
    import secrets

    main(n_iter)

    #print(f"size of all_paths matches?  {"yes" if len(all_paths) == num_walks else "no"}")
    #print(f"number of points matches?  {"yes" if len(all_data[0]) == num_walks * path_length else "no"}")
    #print(f"number of endpoints matches?  {"yes" if len(endpoints[0]) == num_walks * path_length else "no"}")
    #print(f"all_paths = {all_paths}")
    #print(f"all_data = {all_data}")
    #print(f"endpoints = {endpoints}")    if debug:
    #print(f"size of all_data = {len(all_data)}")

    #rest_of_program(main_fig, main_ax, endpoints, all_data)

    #for i in range(0, len(all_data) - 1):
         # create connecting lines
    #    if show_paths:
    #        main_ax.plot([all_data[i][0], all_data[i+1][0]],[all_data[i][1], all_data[i+1]][1],[all_data[i][2], all_data[i+1]][2], color = 'g')
