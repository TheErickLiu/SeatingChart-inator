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
    for generation in range(generations):
        fitnesses = [fitness(tables) for tables in population]
        if generation % 100 == 0:
            print(f'Generation {generation}: Best fitness = {max(fitnesses)}')
        parents = select_parents(population, fitnesses, population_size // 2)
        offspring = crossover(parents, population_size - len(parents))
        for child in offspring:
            mutate(child, mutation_rate)
        population = list(parents) + offspring
    best_solution = population[np.argmax(fitnesses)]
    return best_solution

students = [
    Student('Alice', ['Bob', 'Charlie']),
    Student('Bob', ['Alice', 'David']),
    Student('Charlie', ['Alice']),
    Student('David', ['Bob']),
    Student('Eve', ['Frank']),
    Student('Frank', ['Eve']),
]

'''
student_names = [f'Student{i+1}' for i in range(36)]
students = []
for name in student_names:
    preferences = random.sample(student_names, k=random.randint(0, 5))  # Each student prefers 0 to 5 random other students
    if name in preferences:
        preferences.remove(name)  # Ensure a student does not prefer themselves
    students.append(Student(name, preferences))
'''

num_tables = 2
table_size = 3
population_size = 100
generations = 5000
mutation_rate = 0.1

best_tables = genetic_algorithm(students, num_tables, table_size, population_size, generations, mutation_rate)

for i, table in enumerate(best_tables):
    print(f'Table {i + 1}: {[student.name for student in table.students]}')
