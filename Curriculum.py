from Graphs import Graph


class Curriculum(Graph):

    def __init__(self, x, y, curriculum, subjects):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.subjects = subjects
        self.classes = {i: [] for i in range(x)}
        self.id_to_subject = None
        self.curriculum = curriculum
        self.curriculum_graph = None
        self.transform_to_graph()


    @staticmethod
    def transpose_c(matrix):
        return list(map(list, zip(*matrix)))

    @staticmethod
    def get_row(matrix, row_index):
        row = []
        for list_of_elem in matrix[row_index]:
            for elem in list_of_elem:
                row.append(elem)
        return row

    @staticmethod
    def get_column(matrix, col_index):
        column = []
        for row in matrix:
            for elem in row[col_index]:
                column.append(elem)
        return column

    def get_vertices(self):
        self.curriculum = self.transpose_c(self.curriculum)
        temp_matrix = []
        class_id = 0
        self.classes[class_id].append(0)
        counter = 1
        for row in self.curriculum:
            temp_row = []
            for elem in row:
                temp_new_elem = []
                if elem > 0:
                    for _ in range(elem):
                        temp_new_elem.append(counter)
                        counter += 1
                else:
                    temp_new_elem.append(0)
                temp_row.append(temp_new_elem)
            temp_matrix.append(temp_row)
            self.classes[class_id].append(counter-1)
            class_id += 1
            if class_id < len(self.classes):
                self.classes[class_id].append(counter-1)
        temp_matrix = self.transpose_c(temp_matrix)
        return temp_matrix, counter-1

    def get_connections(self, curriculum_with_vertices, current_v, i, j):
        connections = [v for v in self.get_row(curriculum_with_vertices, i) + self.get_column(curriculum_with_vertices, j) if v != 0 and v != current_v]
        return connections

    def transform_to_graph(self):
        curriculum_with_vertices, num_of_vertices = self.get_vertices()
        self.id_to_subject = {i: "" for i in range(1, num_of_vertices+1)}
        graph = [[0 for _ in range(num_of_vertices)] for _ in range(num_of_vertices)]
        for i in range(self.y):
            for j in range(self.x):
                for current_v in curriculum_with_vertices[i][j]:
                    if current_v == 0:
                        continue
                    self.id_to_subject[current_v] = self.subjects[i]
                    for index in self.get_connections(curriculum_with_vertices, current_v, i, j):
                        graph[current_v-1][index-1] = 1
        self.curriculum_graph = Graph(num_of_vertices, num_of_vertices)
        self.curriculum_graph.read_matrix(graph)

    def transform_coloring_to_timetable(self, coloring):
        timetable = [["---" for _ in range(len(self.classes))] for _ in range(max(coloring))]
        colors_tuple = [(coloring[ind-1], ind) for ind in range(1, len(coloring)+1)]
        current_class = 0
        while current_class < len(self.classes):
            start, end = self.classes[current_class]
            current_class_lessons = colors_tuple[start:end]
            current_class_lessons.sort()
            for lesson in current_class_lessons:
                timetable[lesson[0]-1][current_class] = self.id_to_subject[lesson[1]]
            current_class += 1

        for i in range(len(timetable)):
            if i % 6 == 0:
                print("\n\n")
            print(timetable[i])

    def display_curriculum_graph_matrix(self):
        self.curriculum_graph.display_matrix()

    def display_curriculum_graph_list(self):
        self.curriculum_graph.display_list()
