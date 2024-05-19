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
    all_students_have_preference = True
    for table in tables:
        for student in table.students:
            if any(preference in [s.name for s in table.students] for preference in student.preferences):
                score += 1
            else:
                all_students_have_preference = False

    if all_students_have_preference:
        score += 30

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
            print(f'Generation {generation}: Best score = {best_fitness}')
        parents = select_parents(population, fitnesses, population_size // 2)
        offspring = crossover(parents, population_size - len(parents))
        for child in offspring:
            mutate(child, mutation_rate)
        population = list(parents) + offspring
    return best_solution
  
students = [
    Student('Alice', ['Bob', 'Charlie', 'David']),
    Student('Bob', ['Alice', 'Charlie', 'David']),
    Student('Charlie', ['Alice', 'Bob', 'David']),
    Student('David', ['Alice', 'Bob', 'Charlie']),
    
    Student('Eve', ['Frank', 'Grace', 'Hannah']),
    Student('Frank', ['Eve', 'Grace', 'Hannah']),
    Student('Grace', ['Eve', 'Frank', 'Hannah']),
    Student('Hannah', ['Eve', 'Frank', 'Grace']),
    
    Student('Ivy', ['Jack', 'Kate', 'Leo']),
    Student('Jack', ['Ivy', 'Kate', 'Leo']),
    Student('Kate', ['Ivy', 'Jack', 'Leo']),
    Student('Leo', ['Ivy', 'Jack', 'Kate']),
    
    Student('Mia', ['Nina', 'Oscar', 'Paul']),
    Student('Nina', ['Mia', 'Oscar', 'Paul']),
    Student('Oscar', ['Mia', 'Nina', 'Paul']),
    Student('Paul', ['Mia', 'Nina', 'Oscar']),
    
    Student('Quinn', ['Ruby', 'Sam', 'Tina']),
    Student('Ruby', ['Quinn', 'Sam', 'Tina']),
    Student('Sam', ['Quinn', 'Ruby', 'Tina']),
    Student('Tina', ['Quinn', 'Ruby', 'Sam']),
    
    Student('Uma', ['Violet', 'Will', 'Xander']),
    Student('Violet', ['Uma', 'Will', 'Xander']),
    Student('Will', ['Uma', 'Violet', 'Xander']),
    Student('Xander', ['Uma', 'Violet', 'Will']),
    
    Student('Yara', ['Zack', 'Ava', 'Ben']),
    Student('Zack', ['Yara', 'Ava', 'Ben']),
    Student('Ava', ['Yara', 'Zack', 'Ben']),
    Student('Ben', ['Yara', 'Zack', 'Ava']),
    
    Student('Chloe', ['Dylan', 'Ellie', 'Finn']),
    Student('Dylan', ['Chloe', 'Ellie', 'Finn']),
    Student('Ellie', ['Chloe', 'Dylan', 'Finn']),
    Student('Finn', ['Chloe', 'Dylan', 'Ellie']),
    
    Student('Gina', ['Harry', 'Isla', 'Erick']),
    Student('Harry', ['Gina', 'Isla', 'Erick']),
    Student('Isla', ['Gina', 'Harry', 'Erick']),
    Student('Erick', ['Gina', 'Harry', 'Isla'])
]
num_tables = 9
table_size = 4
population_size = 100
generations = 10000
mutation_rate = 0.1

best_tables = genetic_algorithm(students, num_tables, table_size, population_size, generations, mutation_rate)

for i, table in enumerate(best_tables):
    print(f'Table {i + 1}: {[student.name for student in table.students]}')