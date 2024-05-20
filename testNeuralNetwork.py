import random

class Student:
    def __init__(self, name, friends, random_students=None):
        self.name = name
        self.friends = friends
        self.random_students = random_students if random_students else []

# Initial list of students with friends
students = [
    Student('Alice', ['Bob', 'Charlie', 'David']),
    Student('Bob', ['Alice']),
    Student('Charlie', ['Alice', 'Uma', 'Chloe']),
    Student('David', ['Alice', 'Bob', 'Charlie']),
    Student('Eve', ['Frank', 'Grace', 'Hannah', 'Ivy']),
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
    Student('Erick', ['Ben', 'Xander'])
]

# Adding random students to around a third of the students
num_students = len(students)
students_to_update = random.sample(students, num_students // 3)

for student in students_to_update:
    random_students = random.sample(students, random.randint(1, 2))
    student.random_students = [s.name for s in random_students if s.name != student.name]

# Checking the updated list of students
for student in students:
    print(f"Student('{student.name}', {student.friends}, {student.random_students}),")