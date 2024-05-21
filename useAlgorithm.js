class Student {
    constructor(name, preferences, avoids) {
        this.name = name;
        this.preferences = preferences;
        this.avoids = avoids;
    }
}

class Table {
    constructor(size) {
        this.size = size;
        this.students = [];
    }

    addStudent(student) {
        if (this.students.length < this.size && !this.students.includes(student)) {
            this.students.push(student);
            return true;
        }
        return false;
    }

    removeStudent(student) {
        const index = this.students.indexOf(student);
        if (index !== -1) {
            this.students.splice(index, 1);
            return true;
        }
        return false;
    }

    toString() {
        return `Table(${this.students.map(student => student.name)})`;
    }
}

function calculateGiniCoefficient(data) {
    const sortedData = data.slice().sort((a, b) => a - b);
    const n = data.length;
    const cumulativeData = sortedData.reduce((acc, val) => {
        acc.push((acc.length > 0 ? acc[acc.length - 1] : 0) + val);
        return acc;
    }, []);
    const sumOfProducts = sortedData.reduce((acc, val, i) => acc + (i + 1) * val, 0);
    const cumulativeSum = cumulativeData[cumulativeData.length - 1];
    return (2 * sumOfProducts - (n + 1) * cumulativeSum) / (n * cumulativeSum);
}

function countSatisfiedPreferences(tables) {
    let score = 0;
    const preferenceCounts = [];
    
    for (const table of tables) {
        let tablePreferenceCount = 0;
        for (const student of table.students) {
            for (const preference of student.preferences) {
                if (table.students.some(s => s.name === preference)) {
                    score++;
                    tablePreferenceCount++;
                }
            }
        }
        preferenceCounts.push(tablePreferenceCount);
    }
    
    for (const table of tables) {
        for (const student of table.students) {
            for (const avoid of student.avoids) {
                if (table.students.some(s => s.name === avoid)) {
                    score--;
                }
            }
        }
    }

    const giniCoefficient = calculateGiniCoefficient(preferenceCounts);

    if (giniCoefficient >= 0 && giniCoefficient < 0.5) {
        const reward = 10 - Math.round(giniCoefficient * 10 * 100) / 100;
        score += reward;
    } else {
        const penalty = Math.round(giniCoefficient * 10 * 100) / 100;
        score -= penalty;
    }

    return { score, giniCoefficient };
}

function assignStudentsToTables(students, numTables, tableSize) {
    const tables = Array.from({ length: numTables }, () => new Table(tableSize));
    students = students.slice();
    students.sort(() => Math.random() - 0.5);
    
    for (const student of students) {
        let bestTable = null;
        let maxPreferences = -1;
        
        for (const table of tables) {
            const currentPreferences = table.students.filter(s => student.preferences.includes(s.name)).length;
            if (table.students.length < table.size && currentPreferences > maxPreferences) {
                bestTable = table;
                maxPreferences = currentPreferences;
            }
        }

        if (bestTable) {
            bestTable.addStudent(student);
        }
    }

    return tables;
}

function optimizeSeating(tables, iterations = 5000) {
    let bestTables = tables.map(t => new Table(t.size));
    tables.forEach((table, i) => bestTables[i].students = table.students.slice());
    let bestScore = countSatisfiedPreferences(tables).score;

    for (let i = 0; i < iterations; i++) {
        const [table1, table2] = tables.slice().sort(() => Math.random() - 0.5).slice(0, 2);
        if (table1.students.length === 0 || table2.students.length === 0) continue;

        const student1 = table1.students[Math.floor(Math.random() * table1.students.length)];
        const student2 = table2.students[Math.floor(Math.random() * table2.students.length)];

        table1.removeStudent(student1);
        table2.removeStudent(student2);
        
        table1.addStudent(student2);
        table2.addStudent(student1);

        const newScore = countSatisfiedPreferences(tables).score;
        if (newScore > bestScore) {
            bestScore = newScore;
            bestTables = tables.map(t => new Table(t.size));
            tables.forEach((table, i) => bestTables[i].students = table.students.slice());
        } else {
            table1.removeStudent(student2);
            table2.removeStudent(student1);
            table1.addStudent(student1);
            table2.addStudent(student2);
        }
    }

    return bestTables;
}

function findBestSeating(students, numTables, tableSize, trials = 10) {
    let bestSeating = null;
    let bestScore = -Infinity;

    for (let i = 0; i < trials; i++) {
        let tables = assignStudentsToTables(students, numTables, tableSize);
        tables = optimizeSeating(tables);
        const { score } = countSatisfiedPreferences(tables);
        if (score > bestScore) {
            bestScore = score;
            bestSeating = tables;
        }
    }

    return bestSeating;
}

const students = [
    new Student('Alice', ['Bob', 'Charlie', 'David'], []),
    new Student('Bob', ['Alice'], ['Yara', 'Tina']),
    new Student('Charlie', ['Alice', 'Uma', 'Chloe'], []),
    new Student('David', ['Alice', 'Bob', 'Charlie'], []),
    new Student('Eve', ['Frank', 'Grace', 'Hannah', 'Ivy'], ['Paul', 'Charlie']),
    new Student('Frank', ['Alice', 'Bob', 'Tina', 'Jack'], ['Kate']),
    new Student('Grace', ['Charlie'], ['Violet']),
    new Student('Hannah', ['Jack', 'Uma', 'Chloe', 'Harry'], ['Erick']),
    new Student('Ivy', ['Charlie'], []),
    new Student('Jack', ['Bob', 'Alice', 'David'], ['Tina', 'Ruby']),
    new Student('Kate', ['Frank', 'Leo', 'Gina'], []),
    new Student('Leo', ['Isla', 'Jack', 'Frank', 'Ivy'], []),
    new Student('Mia', ['Ruby', 'Uma'], []),
    new Student('Nina', ['Bob'], ['Ava']),
    new Student('Oscar', ['Violet'], []),
    new Student('Paul', ['Grace'], ['Charlie']),
    new Student('Quinn', ['Tina'], []),
    new Student('Ruby', ['Hannah', 'Grace', 'Kate'], []),
    new Student('Sam', ['Tina', 'Gina', 'Paul', 'Kate'], []),
    new Student('Tina', ['Yara', 'Harry'], []),
    new Student('Uma', ['Alice'], []),
    new Student('Violet', ['Uma', 'Oscar'], ['Frank', 'Ivy']),
    new Student('Will', ['Gina', 'Eve', 'Quinn', 'Alice'], []),
    new Student('Xander', ['Gina', 'Ruby'], []),
    new Student('Yara', ['Ben', 'Hannah'], []),
    new Student('Zack', ['Nina', 'Paul', 'Frank'], []),
    new Student('Ava', ['Paul', 'Sam', 'Oscar', 'Xander'], []),
    new Student('Ben', ['Ava', 'Harry', 'Nina', 'Xander'], ['Ava']),
    new Student('Chloe', ['Sam', 'Ben'], ['Gina', 'Quinn']),
    new Student('Dylan', ['Hannah', 'Bob'], []),
    new Student('Ellie', ['Quinn', 'Alice', 'Tina'], []),
    new Student('Finn', ['Mia', 'Jack', 'Ellie', 'Chloe'], []),
    new Student('Gina', ['Nina', 'Tina', 'Jack'], ['Ruby']),
    new Student('Harry', ['Sam', 'Nina'], []),
    new Student('Isla', ['Ava', 'David', 'Violet'], []),
    new Student('Erick', ['Ben', 'Xander'], [])
];

const numTables = 9;
const tableSize = 4;

const bestSeating = findBestSeating(students, numTables, tableSize, 10);
bestSeating.forEach(table => console.log(table.toString()));
const { score, giniCoefficient } = countSatisfiedPreferences(bestSeating);
console.log(`Best Score: ${score}`);
console.log(`Gini Coefficient: ${giniCoefficient}`);