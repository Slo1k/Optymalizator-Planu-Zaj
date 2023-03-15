# Optymalizator Planu Zajęć
Program służący do układania optymalnego planu zajęć dla szkoły/uczelni z wykorzystaniem kolorowania grafu.

### Autorzy
- Mikołaj Krakowiak
- Jakub Kozłowski

### Podstawy teoretyczne

Układanie planu zajęć jest bardzo ważnym zadaniem realizowanym przez zarządzających dowolną szkołą czy uczelnią. Bez takiego planu trudno wyobrazić sobie pracę instytucji edukacyjnej. Obecnie, zależnie od rodzaju szkoły, plan zajęć jest przygotowywany tylko raz (szkoła podstawowa, gimnazjum) lub więcej razy (liceum ogólnokształcące) w roku szkolnym. Inaczej natomiast będzie w przyszłości, co możemy zauważyć uwzględniając ustalenia reformy systemów edukacji i zatrudniania nauczycieli. Zadanie ułożenia wystarczająco dobrego planu lekcji, w zależności od rozmiaru szkoły i umiejętności układającego, wymaga poświęcenia pracy trwającej od kilku dni do dwóch tygodni, który to czas mógłby być przeznaczony na inne cele. Od momentu nastania ery komputeryzacji naszego życia, a także w ostatnich latach komputeryzacji szkół, pojawiło się wiele komputerowych programów wspomagających układanie planu lekcji. Programy takie są lepsze lub gorsze, bardziej lub mniej przyjazne dla użytkownika, dające w wyniku bardziej lub mniej doskonałe plany. Często zależy to od specyfiki danej instytucji lub od algorytmu użytego do stworzenia programu.

Zadanie układania harmonogramu zajęć ma bardzo ważne praktyczne zastosowania. Było bardzo intensywnie badane i udowodniono, że jest ono NP-trudne. Jest tak z powodu wielu występujących w zadaniu nietrywialnych ograniczeń o różnym charakterze. Pokazano już bardzo wiele algorytmów wykorzystujących znane obszary dziedziny badań operacyjnych i adaptujących nowe. Pierwsze algorytmy zastosowane i wykonywane przy pomocy komputera pojawiły się już we wczesnych latach sześćdziesiątych. W proponowanych przez siebie metodach rozwiązywania problemu układania planu lekcji badacze wykorzystują bardzo często różnego rodzaju algorytmy kolorowania grafu, gdyż jedną z postaci problemu jest graf, przy pomocy którego łatwo można przedstawić konflikty między poszczególnymi zajęciami, klasami czy nauczycielami. Korzysta się również z metod sekwencyjnych. Przeniesienie zachowań organizmów biologicznych na grunt algorytmów pozwoliło, przy rozwiązywaniu omawianego problemu, na zastosowanie algorytmów genetycznych. Używane są również metody lokalnego przeglądu, na przykład symulowanego wyżarzania, metody przeglądu z listą zakazów. Niezmiernie rozprzestrzenione jest podejście hybrydowe, w którym stosowane są algorytmy różnych rodzajów nawzajem się uzupełniających.

Najważniejszym celem niniejszej pracy jest zaprezentowanie algorytmu układania szkolnego planu lekcji, w którym w jednym z etapów wykorzystywane jest kolorowanie grafu. Głównym zadaniem proponowanej metody jest układanie jak najlepszego szkolnego planu lekcji w rozsądnym, z powodów praktycznych, czasie przy uwzględnieniu występujących ograniczeń.

### Etapy procesu układaniu planu zajęć
1. Przekształcenie programu nauczania szkoły do postaci grafu
2. Kolorowanie grafu 
3. Przekształcenie pokolorowanego grafu na plan lekcji

### Przekształcenie programu nauczania szkoły do postaci grafu

W pierwszym kroku przekształcamy program nauczania znajdujący się w tabeli do postaci grafu w następujący sposób:
- każda godzina zajęć jest reprezentowana przez jeden wierzchołek grafu
- każde dwa wierzchołki reprezentujące godziny znajdujące się w tej samej kolumnie tabeli są połączone gałęzią, analogicznie mamy dla godzin z tego samego wiersza

Przykładowe programy nauczania obsługiwane przez nasz program (w nawiasach numery wierzchołków grafu):
<p align="center">
 <img src="https://github.com/Slo1k/Optymalizator-Planu-Zaj-/blob/main/images/program_nauczania.png?raw=true">
</p>

Graf reprezentujący programy nauczania przedstawione powyżej:
<p align="center">
 <img src="https://github.com/Slo1k/Optymalizator-Planu-Zaj-/blob/main/images/graf.png?raw=true">
</p>
Etap ten może wydawać się oczywisty, ale podczas jego realizacji odbywa się uwzględnianie w tworzonym grafie części ograniczeń planu zajęć.
Kod w języku Python odpowiedzialny za transformację programu nauczania do grafu znajduję się poniżej:

```python
import copy
import json
 
 
class Curriculum:
 
    def __init__(self, number_of_classes, number_of_subjects, curriculum, subjects):
        self.number_of_classes = number_of_classes
        self.number_of_subjects = number_of_subjects
        self.curriculum = curriculum
        self.subjects = subjects
        self.timetable = None
        self.quality_tmp = 0
 
        self.classes = {i: [] for i in range(number_of_classes)}
        self.id_to_subject = None
        self.adj_matrix = None
        self.transform_to_graph()
 
    @staticmethod
    def transpose(matrix):
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
        self.curriculum = self.transpose(self.curriculum)
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
        temp_matrix = self.transpose(temp_matrix)
        return temp_matrix, counter-1
 
    def get_connections(self, curriculum_with_vertices, current_v, i, j):
        connections = [v for v in self.get_row(curriculum_with_vertices, i) + self.get_column(curriculum_with_vertices, j) if v != 0 and v != current_v]
        return connections
 
    def transform_to_graph(self):
        curriculum_with_vertices, num_of_vertices = self.get_vertices()
        self.id_to_subject = {i: "" for i in range(1, num_of_vertices+1)}
        matrix = [[0 for _ in range(num_of_vertices)] for _ in range(num_of_vertices)]
        for i in range(self.number_of_subjects):
            for j in range(self.number_of_classes):
                for current_v in curriculum_with_vertices[i][j]:
                    if current_v == 0:
                        continue
                    self.id_to_subject[current_v] = self.subjects[i]
                    for index in self.get_connections(curriculum_with_vertices, current_v, i, j):
                        matrix[current_v-1][index-1] = 1
        self.adj_matrix = matrix
```
### Kolorowanie grafu

Wierzchołki grafu, uzyskanego w poprzednim kroku, kolorujemy w taki sposób, aby każde dwa sąsiednie miały różne kolory. W naszym projekcie zaimplementowaliśmy dwie metody kolorowania grafów:

- algorytm zachłanny
- algorytm genetyczny

Kod w języku Python odpowiedzialny za kolorowanie grafu znajduję się poniżej:
```python
import random
 
 
class Coloring:
 
    def __init__(self, adj_matrix):
        self.adj_matrix = adj_matrix
        self.result = None
        self.n = len(adj_matrix)
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
```

### Przekształcenie pokolorowanego grafu na plan lekcji

Ponieważ wierzchołki jednego koloru reprezentują zajęcia, które mogą się odbywać jednocześnie, możemy więc teraz przenieść wszystkie zbiory pokolorowanych wierzchołków (odpowiednio je opisując) w odpowiednie miejsca do tablicy planu zajęć.


Kod w języku Python odpowiedzialny za przekształcenie pokolorowanego grafu na plan lekcji znajduję się poniżej (UWAGA jest to ciąg dalszy kodu klasy Curriculum):
```python
import copy
import json
 
 
class Curriculum:
 
...
 
 
    def transform_colors_to_timetable(self, colors, hours_per_day):
        self.timetable = [["---" for _ in range(len(self.classes))] for _ in range(max(colors))]
        colors_tuple = [(colors[ind-1], ind) for ind in range(1, len(colors)+1)]
        current_class = 0
        while current_class < len(self.classes):
            start, end = self.classes[current_class]
            current_class_lessons = colors_tuple[start:end]
            current_class_lessons.sort()
            for lesson in current_class_lessons:
                self.timetable[lesson[0]-1][current_class] = self.id_to_subject[lesson[1]]
            current_class += 1
 
        timetable_data = {}
        day_num = 1
        day = []
        for i in range(len(self.timetable)):
            if i % hours_per_day == 0 and i != 0:
                timetable_data[str(day_num)] = copy.deepcopy(day)
                print("\n\n")
                day_num += 1
                day.clear()
            day.append(self.timetable[i])
            print(self.timetable[i])
 
        if day:
            empty_hours = [["---"] for _ in range(self.number_of_classes)]
            while (len(day)) < hours_per_day:
                day.append(empty_hours)
                self.quality_tmp += 1
            timetable_data[str(day_num)] = copy.deepcopy(day)
 
        return json.dumps(timetable_data)
 
    def get_timetable_quality(self):
        size = len(self.timetable)
        if self.quality_tmp > 0:
            size = self.quality_tmp
        windows = 0
        lessons = 0
        for row in self.timetable[:-size]:
            for les in row:
                if les == "---":
                    windows += 1
                else:
                    lessons += 1
 
        quality = lessons / (lessons + windows) * 100
        return f"{round(quality, 2)}%"
 
    def get_number_of_classes(self):
        return self.number_of_classes
 
    def display_curriculum_graph_matrix(self):
        self.adj_matrix.display_matrix()
 
    def display_curriculum_graph_list(self):
        self.adj_matrix.display_list()
```

### Format pliku JSON danych wejściowych

Nasz program umożliwia również możliwość wczytania danych wejściowych w formacie JSON, co pozwala zaoszczędzić na czasie który trzeba by było poświęcić na uzupełnienie programu nauczania.

```
{
 "subject_hours": [["1", "3", "2"], ["4", "3", "5"]], - reprezentuje liczbę godzin danych przedmiotów dla danej klasy, np '...["1", "3", "2"],.. oznacza 1 godzinę przedmiotu X w klasie 1, 3 w klasie 2 i 2 w klasie 2
 "subjects": ["Matematyka", "Biologia"], - reprezentuje przedmioty
 "lessons_hours": [["8:00", "9:00"], ["9:10", "10:10"], ["11:20", "12:20"]] - reprezentuje godziny lekcyjne
}
```

### Wybór technologii

- Python 3.9 + Flask
- JavaScript + HTML

### Prezentacja projektu

<p align="center">
 <img src="https://github.com/Slo1k/Optymalizator-Planu-Zaj-/blob/main/images/program.png?raw=true">
</p>

### Przykładowe uruchomienia naszego programu

- Dla niewielkiej instancji:
<p align="center">
 <img src="https://github.com/Slo1k/Optymalizator-Planu-Zaj-/blob/main/images/wynik1.png?raw=true">
</p>

- Dla większej instancji reprezentującej rzeczywisty program nauczania:
<p align="center">
 <img src="https://github.com/Slo1k/Optymalizator-Planu-Zaj-/blob/main/images/wynik2.png?raw=true">
</p>

### Wnioski końcowe

Grafy tworzone na bazie programu nauczania są zwykle grafami niezbyt gęstymi (gęstość 20%-50%), dlatego też wyniki algorytmu genetycznego są często gorsze od wyników algorytmu zachłannego. Wynikać może to również z tego że wartość populacji jak i liczba generacji była stosunkowa niewielka (200), gdyby zwiększyć obie te zmienne szansa na uzyskanie lepszego rozwiązania wzrasta. Również czas wykonania algorytmu genetycznego jest dużo większy od czasu wykonania algorytmu zachłannego co sprawia że bardziej efektywnym algorytmem w przypadku kolorowania takich grafów jest algorytm zachłanny. Możemy jednak zauważyć że w wyniku randomizacji sposobu pokolorowania grafu w przypadku algorytmu genetycznego, niemożliwym wręcz jest wygenerowanie planu zajęć w którym przykładowo język polski odbywałby się przez 6 godzin z rzędu. Takie zachowanie algorytmu genetycznego może być dla nas korzystne gdyż takie nagromadzenie się zajęć z jednego przedmiotu może negatywnie odbić się na jakości kształcenia.

### Możliwe dalsze ścieżki rozwoju projektu
- Dodanie powiązania z nauczycielami
- Dodanie możliwości podziału klas na podgrupy
- Dodanie metod suboptymalnego kolorowanie grafu w celu polepszenia jakości rozwiązań
