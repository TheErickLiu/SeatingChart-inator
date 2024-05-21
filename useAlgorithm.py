import random
import numpy as np

class Student:
    def __init__(self, name, preferences, avoids):
        self.name = name
        self.preferences = preferences
        self.avoids = avoids

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

    def __repr__(self):
        return f"Table({[student.name for student in self.students]})"

def calculate_gini_coefficient(data):
    sorted_data = sorted(data)
    n = len(data)
    cumulative_data = np.cumsum(sorted_data)
    return (2 * np.sum((i + 1) * sorted_data[i] for i in range(n)) - (n + 1) * cumulative_data[-1]) / (n * cumulative_data[-1])

def count_satisfied_preferences(tables):
    score = 0
    preference_counts = []
    
    for table in tables:
        table_preference_count = 0
        for student in table.students:
            for preference in student.preferences:
                if preference in [s.name for s in table.students]:
                    score += 1
                    table_preference_count += 1
        preference_counts.append(table_preference_count)
    
    for table in tables:
        for student in table.students:
            for avoid in student.avoids:
                if avoid in [s.name for s in table.students]:
                    score -= 1
    
    gini_coefficient = calculate_gini_coefficient(preference_counts)
    
    if gini_coefficient >= 0 and gini_coefficient < 0.5:
        reward = 10 - round(gini_coefficient, 2) * 10
        score += reward
    else:
        penalty = round(gini_coefficient, 2) * 10
        score -= penalty
    
    return score, gini_coefficient

def assign_students_to_tables(students, num_tables, table_size):
    tables = [Table(table_size) for _ in range(num_tables)]
    random.shuffle(students)
    
    for student in students:
        best_table = None
        max_preferences = -1
        
        for table in tables:
            current_preferences = sum(1 for s in table.students if s.name in student.preferences)
            
            if len(table.students) < table.size and current_preferences > max_preferences:
                best_table = table
                max_preferences = current_preferences
        
        if best_table:
            best_table.add_student(student)
    
    return tables

def optimize_seating(tables, iterations=5000):
    best_tables = tables
    best_score = count_satisfied_preferences(tables)[0]
    
    for _ in range(iterations):
        table1, table2 = random.sample(tables, 2)
        if not table1.students or not table2.students:
            continue

        student1 = random.choice(table1.students)
        student2 = random.choice(table2.students)

        table1.remove_student(student1)
        table2.remove_student(student2)
        
        table1.add_student(student2)
        table2.add_student(student1)
        
        new_score = count_satisfied_preferences(tables)[0]
        if new_score > best_score:
            best_score = new_score
            best_tables = [Table(t.size) for t in tables]
            for t, bt in zip(tables, best_tables):
                bt.students = t.students.copy()
        else:
            table1.remove_student(student2)
            table2.remove_student(student1)
            table1.add_student(student1)
            table2.add_student(student2)
    
    return best_tables

def find_best_seating(students, num_tables, table_size, trials=10):
    best_seating = None
    best_score = float('-inf')
    
    for _ in range(trials):
        tables = assign_students_to_tables(students, num_tables, table_size)
        tables = optimize_seating(tables)
        score = count_satisfied_preferences(tables)[0]
        if score > best_score:
            best_score = score
            best_seating = tables
    
    return best_seating

students = [
    Student('Alice', ['Bob', 'Charlie', 'David'], []),
    Student('Bob', ['Alice'], ['Yara', 'Tina']),
    Student('Charlie', ['Alice', 'Uma', 'Chloe'], []),
    Student('David', ['Alice', 'Bob', 'Charlie'], []),
    Student('Eve', ['Frank', 'Grace', 'Hannah', 'Ivy'], ['Paul', 'Charlie']),
    Student('Frank', ['Alice', 'Bob', 'Tina', 'Jack'], ['Kate']),
    Student('Grace', ['Charlie'], ['Violet']),
    Student('Hannah', ['Jack', 'Uma', 'Chloe', 'Harry'], ['Erick']),
    Student('Ivy', ['Charlie'], []),
    Student('Jack', ['Bob', 'Alice', 'David'], ['Tina', 'Ruby']),
    Student('Kate', ['Frank', 'Leo', 'Gina'], []),
    Student('Leo', ['Isla', 'Jack', 'Frank', 'Ivy'], []),
    Student('Mia', ['Ruby', 'Uma'], []),
    Student('Nina', ['Bob'], ['Ava']),
    Student('Oscar', ['Violet'], []),
    Student('Paul', ['Grace'], ['Charlie']),
    Student('Quinn', ['Tina'], []),
    Student('Ruby', ['Hannah', 'Grace', 'Kate'], []),
    Student('Sam', ['Tina', 'Gina', 'Paul', 'Kate'], []),
    Student('Tina', ['Yara', 'Harry'], []),
    Student('Uma', ['Alice'], []),
    Student('Violet', ['Uma', 'Oscar'], ['Frank', 'Ivy']),
    Student('Will', ['Gina', 'Eve', 'Quinn', 'Alice'], []),
    Student('Xander', ['Gina', 'Ruby'], []),
    Student('Yara', ['Ben', 'Hannah'], []),
    Student('Zack', ['Nina', 'Paul', 'Frank'], []),
    Student('Ava', ['Paul', 'Sam', 'Oscar', 'Xander'], []),
    Student('Ben', ['Ava', 'Harry', 'Nina', 'Xander'], ['Ava']),
    Student('Chloe', ['Sam', 'Ben'], ['Gina', 'Quinn']),
    Student('Dylan', ['Hannah', 'Bob'], []),
    Student('Ellie', ['Quinn', 'Alice', 'Tina'], []),
    Student('Finn', ['Mia', 'Jack', 'Ellie', 'Chloe'], []),
    Student('Gina', ['Nina', 'Tina', 'Jack'], ['Ruby']),
    Student('Harry', ['Sam', 'Nina'], []),
    Student('Isla', ['Ava', 'David', 'Violet'], []),
    Student('Erick', ['Ben', 'Xander'], [])
]

num_tables = 9
table_size = 4

best_seating = find_best_seating(students, num_tables, table_size, trials=10)
for table in best_seating:
    print(table)
print(f"Best Score: {count_satisfied_preferences(best_seating)[0]}")
print(f"Gini Coefficient: {count_satisfied_preferences(best_seating)[1]}")
      