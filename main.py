# Import necessary libraries
import os
import random
import copy
import time


# Class representing a word in the crossword
class Word:
    def __init__(self, string):
        # Initialize word attributes with random values
        self.z = random.choice([0, 1])
        self.x = random.randint(0, (19 - len(string) + 1) if self.z == 1 else 19)
        self.y = random.randint(0, (19 - len(string) + 1) if self.z == 0 else 19)
        self.string = string


# Class representing a genome (collection of words)
class Genome:
    def __init__(self, words):
        self.words = words


# Class representing a population of genomes
class Population:
    def __init__(self, word_list, size):
        # Create a population of genomes with random words
        self.genomes = [self.create_genome(word_list) for _ in range(size)]

    def create_genome(self, word_list):
        # Create a genome with random words from the word list
        words = [Word(word) for word in word_list]
        return Genome(words)


# Function for crossover between two genomes
def crossover(genome1, genome2):
    new_genome3 = Genome([])
    new_genome4 = Genome([])
    delimetr = random.randint(1, len(genome1.words) - 1)
    for i in range(len(genome1.words)):
        # Swap words between genomes at the delimiter index
        if i < delimetr:
            new_genome3.words.append(genome1.words[i])
            new_genome4.words.append(genome2.words[i])
        else:
            new_genome3.words.append(genome2.words[i])
            new_genome4.words.append(genome1.words[i])
    return new_genome3, new_genome4


# Function for mutating a genome
def mutate_genome(genome):
    if random.random() < 0.6:
        # Randomly mutate a word in the genome
        id = random.randint(0, len(genome.words) - 1)
        word = genome.words[id]
        word.z = random.choice([0, 1])
        word.x = random.randint(0, 19 - len(word.string) if word.z == 1 else 19)
        word.y = random.randint(0, 19 - len(word.string) if word.z == 0 else 19)
    return genome


# Function to check if two words intersect in the crossword grid
def are_words_intersect(a, b):
    # Check if two words intersect based on their coordinates and orientation
    x, y, w = a.x, a.y, len(a.string)
    x2, y2, w2 = b.x, b.y, len(b.string)
    end_x = x + (w - 1 if a.z == 1 else 0)
    end_y = y + (w - 1 if a.z == 0 else 0)

    end_x2 = x2 + (w2 - 1 if b.z == 1 else 0)
    end_y2 = y2 + (w2 - 1 if b.z == 0 else 0)

    if a.z == b.z:
        return False

    if a.z == 1 and (x <= x2 <= end_x) and (y2 <= y <= end_y2):
        return True

    if b.z == 1 and (x2 <= x <= end_x2) and (y <= y2 <= end_y):
        return True

    return False


# Function to check if two words are parallel in the crossword grid
def are_words_parallel(a, b):
    # Check if two words are parallel based on their coordinates and orientation
    x, y, w = a.x, a.y, len(a.string)
    x2, y2, w2 = b.x, b.y, len(b.string)
    end_x = x + (w - 1 if a.z == 1 else 0)
    end_y = y + (w - 1 if a.z == 0 else 0)

    end_x2 = x2 + (w2 - 1 if b.z == 1 else 0)
    end_y2 = y2 + (w2 - 1 if b.z == 0 else 0)

    if a.z == b.z:
        if a.z == 1 and (abs(y - y2) <= 1) and (
                (x2 <= x <= end_x2) or (x2 <= end_x <= end_x2) or (x <= x2 <= end_x) or (x <= end_x2 <= end_x)):
            return True
        if a.z == 1 and (y == y2) and (
                (x2 - 1 <= x <= end_x2 + 1) or (x2 - 1 <= end_x <= end_x2 + 1) or (x - 1 <= x2 <= end_x + 1) or (
                x - 1 <= end_x2 <= end_x + 1)):
            return True

        if a.z == 0 and (abs(x - x2) <= 1) and (
                (y2 <= y <= end_y2) or (y2 <= end_y <= end_y2) or (y <= y2 <= end_y) or (y <= end_y2 <= end_y)):
            return True

        if a.z == 0 and (x == x2) and (
                (y2 - 1 <= y <= end_y2 + 1) or (y2 - 1 <= end_y <= end_y2 + 1) or (y - 1 <= y2 <= end_y + 1) or (
                y - 1 <= end_y2 <= end_y + 1)):
            return True

    return False


# Function to check if two words are near to intersecting in the crossword grid
def are_words_near_to_intersect(a, b):
    # Check if two words are near to intersecting based on their coordinates and orientation
    x, y, w = a.x, a.y, len(a.string)
    x2, y2, w2 = b.x, b.y, len(b.string)
    end_x = x + (w - 1 if a.z == 1 else 0)
    end_y = y + (w - 1 if a.z == 0 else 0)

    end_x2 = x2 + (w2 - 1 if b.z == 1 else 0)
    end_y2 = y2 + (w2 - 1 if b.z == 0 else 0)

    if a.z != b.z:
        if a.z == 1 and (abs(x2 - x) == 1 or abs(x2 - end_x) == 1) and (y2 <= y <= end_y2):
            return True

        if b.z == 1 and (abs(x - x2) == 1 or abs(x - end_x2) == 1) and (y <= y2 <= end_y):
            return True

        if a.z == 0 and (abs(y2 - y) == 1 or abs(y2 - end_y) == 1) and (x2 <= x <= end_x2):
            return True

        if b.z == 0 and (abs(y - y2) == 1 or abs(y - end_y2) == 1) and (x <= x2 <= end_x):
            return True

    return False


# Function to evaluate the fitness of a genome in creating a valid crossword
def evaluate_fitness(genome):
    # Evaluate fitness based on various criteria and return the error score
    crossword = Crossword()
    errors = 0

    for word in genome.words:

        x, y = word.x, word.y

        for letter in word.string:
            if crossword.grid[x][y] != '*' and crossword.grid[x][y] != letter:
                errors += 1
            if word.z == 1:
                x += 1
            else:
                y += 1

        crossword.add_word(word)

    free_words = 0
    parallel = 0
    not_intersect = 0
    for i in range(len(genome.words)):
        is_free = 1
        for j in range(i + 1, len(genome.words)):
            word1 = genome.words[i]
            word2 = genome.words[j]
            if are_words_intersect(word1, word2):
                is_free = 0
            if are_words_parallel(word1, word2):
                parallel += 1
            if are_words_near_to_intersect(word1, word2):
                not_intersect += 1
        for j in range(len(genome.words)):
            if j == i:
                continue
            if are_words_intersect(genome.words[i], genome.words[j]):
                is_free = 0
        free_words += is_free

    errors += free_words * 7
    errors += crossword.is_graph_connected() * 30
    errors += parallel * 15
    errors += not_intersect * 20

    return errors


# Class representing a crossword grid
class Crossword:
    def __init__(self, size=20):
        # Initialize the crossword grid with empty cells
        self.size = size
        self.grid = [['*'] * size for _ in range(size)]

    def add_word(self, word):
        # Add a word to the crossword grid
        x, y = word.x, word.y

        if word.z == 0:
            for letter in word.string:
                self.grid[x][y] = letter
                y += 1
        else:
            for letter in word.string:
                self.grid[x][y] = letter
                x += 1

    def is_graph_connected(self):
        # Check if the crossword grid forms a connected graph
        visited = set()
        cnt = 0

        def dfs(x, y):
            if (x, y) in visited or x < 0 or x >= self.size or y < 0 or y >= self.size or self.grid[x][y] == '*':
                return
            visited.add((x, y))
            dfs(x + 1, y)
            dfs(x - 1, y)
            dfs(x, y + 1)
            dfs(x, y - 1)

        for x in range(self.size):
            for y in range(self.size):
                if (x, y) in visited:
                    continue
                if self.grid[x][y] != '*':
                    cnt += 1
                    dfs(x, y)

        return cnt - 1


# Function to select the best genomes from a population based on fitness
def select_best_genomes(population, num_best):
    # Sort genomes based on fitness and return the top ones
    sorted_genomes = sorted(population.genomes, key=evaluate_fitness)
    return sorted_genomes[:num_best]


# Main function to execute the crossword generation process
def main():
    # Set input and output directories
    input_directory = 'input'
    output_directory = 'output'
    # Check and create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through input files in the input directory
    for input_file in sorted(os.listdir(input_directory)):
        if input_file.endswith('.txt'):
            # Generate output path and read the input word list
            input_path = os.path.join(input_directory, input_file)
            output_path = os.path.join(output_directory, input_file.replace('input', 'output'))
            word_list = read_input_file(input_path)

            # Set population size and number of generations
            start_time = time.time()
            population_size = 100
            num_generations = 20001
            population = Population(word_list, population_size)

            # Iterate through generations
            for generation in range(num_generations):

                # Reinitialize population every 2000 generations
                # Select the best genomes, perform crossover and mutation
                best_genomes = select_best_genomes(population, 20)

                if generation % 1000 == 0:
                    print(f'{generation} {evaluate_fitness(best_genomes[0])}')
                if evaluate_fitness(best_genomes[0]) == 0:
                    break

                new_population = Population(word_list, 0)
                for i in range(8):
                    for j in range(i + 1, 8):
                        parent1 = copy.deepcopy(best_genomes[i])
                        parent2 = copy.deepcopy(best_genomes[j])
                        child1, child2 = crossover(parent1, parent2)
                        new_population.genomes.append(child1)

                for i in population.genomes:
                    new_population.genomes.append(copy.deepcopy(i))

                population.genomes = select_best_genomes(new_population, 100)
                for genome in population.genomes:
                    mutate_genome(genome)

            # Measure and print execution time, save output
            end_time = time.time()
            print(len(word_list), round(end_time - start_time, 2))
            save_output(output_path, select_best_genomes(population, 1)[0], round(end_time - start_time, 2))


# Function to read the input file and return the word list
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        word_list = file.read().splitlines()
    return word_list


# Function to save the output to a file
def save_output(file_path, crossword, tm):
    with open(file_path, 'w') as file:
        file.write(f'time: {tm}\n')
        for word in crossword.words:
            file.write(f'{word.x} {word.y} {word.z}\n')


if __name__ == "__main__":
    main()
