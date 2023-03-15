import random


class Coloring:

    def __init__(self, graph):
        self.graph = graph
        self.adj_matrix = graph.adj_matrix
        self.result = None
        self.n = graph.x
        self.max_num_colors = 1
        for i in range(self.n):
            if sum(self.adj_matrix[i]) > self.max_num_colors:
                self.max_num_colors = sum(self.adj_matrix[i]) + 1

    def random_coloring(self, number_of_colors):
        colors = []
        for i in range(self.n):
            colors.append(random.randint(1, number_of_colors))
        return colors

    def fitness(self, colors):
        fitness = 0
        for i in range(self.n):
            for j in range(i, self.n):
                if colors[i] == colors[j] and self.adj_matrix[i][j] == 1:
                    fitness += 1
        return fitness

    def crossover(self, parent1, parent2):
        position = random.randint(2, self.n - 2)
        child1 = []
        child2 = []
        for i in range(position + 1):
            child1.append(parent1[i])
            child2.append(parent2[i])
        for i in range(position + 1, self.n):
            child1.append(parent2[i])
            child2.append(parent1[i])
        return child1, child2

    def mutation1(self, colors, number_of_colors):
        probability = 0.4
        check = random.uniform(0, 1)
        if check <= probability:
            position = random.randint(0, self.n - 1)
            colors[position] = random.randint(1, number_of_colors)
        return colors
    
    def mutation2(self, colors, number_of_colors):
        probability = 0.2
        check = random.uniform(0, 1)
        if check <= probability:
            position = random.randint(0, self.n - 1)
            colors[position] = random.randint(1, number_of_colors)
        return colors

    def tournament_selection(self, population, population_size):
        new_population = []
        for j in range(2):
            random.shuffle(population)
            for i in range(0, population_size - 1, 2):
                if self.fitness(population[i]) < self.fitness(population[i + 1]):
                    new_population.append(population[i])
                else:
                    new_population.append(population[i + 1])
        return new_population

    def roulette_wheel_selection(self, population):
        total_fitness = 0
        for colors in population:
            total_fitness += 1 / (1 + self.fitness(colors))
        cumulative_fitness = []
        cumulative_fitness_sum = 0
        for i in range(len(population)):
            cumulative_fitness_sum += 1 / (1 + self.fitness(population[i])) / total_fitness
            cumulative_fitness.append(cumulative_fitness_sum)

        new_population = []
        for i in range(len(population)):
            roulette = random.uniform(0, 1)
            for j in range(len(population)):
                if roulette <= cumulative_fitness[j]:
                    new_population.append(population[j])
                    break
        return new_population
    
    def run_genetic(self, population_size, num_of_gen):
        condition = True
        result = None
        number_of_colors = self.max_num_colors

        while condition and number_of_colors > 0:

            gen = 0
            population = []

            for i in range(population_size):
                colors = self.random_coloring(number_of_colors)
                population.append(colors)

            best_fitness = self.fitness(population[0])
            fittest_colors = population[0]
            while best_fitness != 0 and gen != num_of_gen:
                gen += 1
                # population = self.tournament_selection(population)
                population = self.roulette_wheel_selection(population)
                new_population = []
                random.shuffle(population)
                for i in range(0, population_size - 1, 2):
                    child1, child2 = self.crossover(population[i], population[i + 1])
                    new_population.append(child1)
                    new_population.append(child2)
                for colors in new_population:
                    if gen < 20:
                        colors = self.mutation1(colors, number_of_colors)
                    else:
                        colors = self.mutation2(colors, number_of_colors)
                population = new_population
                best_fitness = self.fitness(population[0])
                fittest_colors = population[0]
                for colors in population:
                    if self.fitness(colors) < best_fitness:
                        best_fitness = self.fitness(colors)
                        fittest_colors = colors
                        if best_fitness == 0:
                            result = fittest_colors
            if best_fitness != 0:
                condition = False
            else:
                number_of_colors -= 1
        return result

    def run_greedy(self):
        colors = [0 for _ in range(self.n)]
        colors[0] = 1
        for i in range(1, self.n):
            for k in range(1, self.n+1):
                good = True
                for j in range(0, i):
                    if self.adj_matrix[i][j] == 1 and colors[j] == k:
                        good = False
                        break
                if good:
                    colors[i] = k
                    break
        return colors


