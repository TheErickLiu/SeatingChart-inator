import random
import numpy as np

class Student:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences

class Table:
    def __init__(self, size):
        self.size = size
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.size and student not in self.students:
            self.students.append(student)
            return True
        return False

    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
            return True
        return False

def generate_initial_population(students, num_tables, table_size, population_size):
    population = []
    for _ in range(population_size):
        tables = [Table(table_size) for _ in range(num_tables)]
        shuffled_students = students[:]
        random.shuffle(shuffled_students)
        for student in shuffled_students:
            added = False
            while not added:
                table = random.choice(tables)
                added = table.add_student(student)
        population.append(tables)
    return population

def fitness(tables):
    score = 0
    for table in tables:
        for student in table.students:
            for preference in student.preferences:
                if preference in [s.name for s in table.students]:
                    score += 1
    return score

def select_parents(population, fitnesses, num_parents):
    fitnesses = np.array(fitnesses)
    fitnesses = fitnesses / np.sum(fitnesses)
    parents_indices = np.random.choice(range(len(population)), size=num_parents, p=fitnesses, replace=False)
    parents = [population[i] for i in parents_indices]
    return parents

def crossover(parents, num_offspring):
    offspring = []
    for _ in range(num_offspring):
        parent1, parent2 = random.sample(parents, 2)
        child_tables = [Table(table.size) for table in parent1]
        students = [student for table in parent1 for student in table.students]
        random.shuffle(students)
        for table in child_tables:
            while len(table.students) < table.size and students:
                student = students.pop()
                table.add_student(student)
        offspring.append(child_tables)
    return offspring

def mutate(tables, mutation_rate):
    for table in tables:
        if len(table.students) > 0:
            for i in range(len(table.students)):
                if random.random() < mutation_rate:
                    other_table = random.choice(tables)
                    if other_table != table and len(other_table.students) > 0:
                        swap_with = random.randint(0, len(other_table.students) - 1)
                        table.students[i], other_table.students[swap_with] = other_table.students[swap_with], table.students[i]

def genetic_algorithm(students, num_tables, table_size, population_size, generations, mutation_rate):
    population = generate_initial_population(students, num_tables, table_size, population_size)
    best_solution = None
    best_fitness = -1
    for generation in range(generations):
        fitnesses = [fitness(tables) for tables in population]
        current_best_fitness = max(fitnesses)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_solution = population[np.argmax(fitnesses)]
        if generation % 100 == 0:
            print(f'Generation {generation}: Best fitness = {best_fitness}')
        parents = select_parents(population, fitnesses, population_size // 2)
        offspring = crossover(parents, population_size - len(parents))
        for child in offspring:
            mutate(child, mutation_rate)
        population = list(parents) + offspring
    return best_solution
  
students = [
    Student('Alice', ['Paul', 'Oscar', 'Kate']),
    Student('Bob', ['Dylan', 'Uma', 'Tina', 'David']),
    Student('Charlie', ['Eve', 'Frank']),
    Student('David', ['Leo']),
    Student('Eve', ['Dylan']),
    Student('Frank', ['Alice', 'Bob', 'Tina', 'Jack']),
    Student('Grace', ['Charlie']),
    Student('Hannah', ['Jack', 'Uma', 'Chloe', 'Harry']),
    Student('Ivy', ['Charlie']),
    Student('Jack', ['Bob', 'Alice', 'David']),
    Student('Kate', ['Frank', 'Leo', 'Gina']),
    Student('Leo', ['Isla', 'Jack', 'Frank', 'Ivy']),
    Student('Mia', ['Ruby', 'Uma']),
    Student('Nina', ['Bob']),
    Student('Oscar', ['Violet']),
    Student('Paul', ['Grace']),
    Student('Quinn', ['Tina']),
    Student('Ruby', ['Hannah', 'Grace', 'Kate']),
    Student('Sam', ['Tina', 'Gina', 'Paul', 'Kate']),
    Student('Tina', ['Yara', 'Harry']),
    Student('Uma', ['Alice']),
    Student('Violet', ['Uma', 'Oscar']),
    Student('Will', ['Gina', 'Eve', 'Quinn', 'Alice']),
    Student('Xander', ['Gina', 'Ruby']),
    Student('Yara', ['Ben', 'Hannah']),
    Student('Zack', ['Nina', 'Paul', 'Frank']),
    Student('Ava', ['Paul', 'Sam', 'Oscar', 'Xander']),
    Student('Ben', ['Ava', 'Harry', 'Nina', 'Xander']),
    Student('Chloe', ['Sam', 'Ben']),
    Student('Dylan', ['Hannah', 'Bob']),
    Student('Ellie', ['Quinn', 'Alice', 'Tina']),
    Student('Finn', ['Mia', 'Jack', 'Ellie', 'Chloe']),
    Student('Gina', ['Nina', 'Tina', 'Jack']),
    Student('Harry', ['Sam', 'Nina']),
    Student('Isla', ['Ava', 'David', 'Violet']),
]
num_tables = 9
table_size = 4
population_size = 50
generations = 5000
mutation_rate = 0.1

best_tables = genetic_algorithm(students, num_tables, table_size, population_size, generations, mutation_rate)

for i, table in enumerate(best_tables):
    print(f'Table {i + 1}: {[student.name for student in table.students]}')