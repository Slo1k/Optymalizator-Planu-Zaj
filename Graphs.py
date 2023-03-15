from collections import defaultdict


class Graph:

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.adj_matrix = [[0 for _ in range(x)] for _ in range(y)]
        self.adj_list = defaultdict(list)

    def read_matrix_from_file(self, source):
        with open(source) as file:
            temp = []
            for row in file:
                temp.append(list(map(int, row.split())))
            self.adj_matrix = temp
            self.matrix_to_list()

    def read_matrix(self, matrix):
        self.adj_matrix = matrix
        self.matrix_to_list()

    def transpose(self):
        self.adj_matrix = [list(i) for i in zip(*self.adj_matrix)]

    def matrix_to_list(self):
        for i in range(self.x):
            for j in range(self.y):
                if self.adj_matrix[i][j] != 0:
                    self.adj_list[i].append(j)

    def display_matrix(self):
        for row in self.adj_matrix:
            print(row)

    def display_list(self):
        print(self.adj_list)
        for k, v in self.adj_list.items():
            print(k, v)
