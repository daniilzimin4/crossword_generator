
# Introduction

This document provides an explanation of the Python code for generating
crosswords using a genetic algorithm.

# Word and Genome Classes

The `Word` class represents a word in the crossword. It randomly assigns
attributes such as orientation (`z`), starting coordinates (`x`, `y`),
and the actual word (`string`). The `Genome` class represents a full
crossword of words.

    class Word:
        def __init__(self, string):
            # ...

    class Genome:
        def __init__(self, words):
            # ...

# Population Class

The `Population` class initializes a population of `Genome` instances
with random words.

    class Population:
        def __init__(self, word_list, size):
            # ...

# Crossover Function

The `crossover` function combines two parent genomes to create two new
genomes. A random delimiter is chosen, and words before the delimiter
are taken from one parent, while words after the delimiter are taken
from the other.

    def crossover(genome1, genome2):
        # ...

# Mutation Function

The `mutate_genome` function randomly modifies a word’s attributes in a
genome based on a probability less than 0.6. Only one word in crossword
will be modified with new random *x*, *y*, *z* coordinates.

    def mutate_genome(genome):
        # ...

# Fitness Evaluation

The `evaluate_fitness` function assesses the fitness of a genome based
on various criteria, including word intersections, parallelism, and
connectedness of the crossword grid. Fitness function calculates count
of errors in crossword. More detailed:

1.  1 error for incorrect intersection, when 2 words with different
    orientation cover the same cell with two different letters

2.  7 errors for each word does not intersect any others and forms a new
    connectivity component

3.  30 errors for each additional connectivity component starting from
    the second one

4.  15 errors for parallel words that lie next to each other

5.  20 errors for two words that do not intersect, but touch each other
    and have different orientations

<!-- -->

    def evaluate_fitness(genome):
        # ...

# Crossword Class

The `Crossword` class represents the crossword grid and provides methods
for adding words and checking graph connectivity. Checking that graph is
connected, calculate number of components. Parallel words considering
like connected.

    class Crossword:
        def __init__(self, size=20):
            # ...

# Selection and Main Loop

The `select_best_genomes` function chooses the best genomes from a
population based on fitness. The `main` function orchestrates the main
algorithm, creating and evolving populations. Generating of new
population executes by next rules:

1.  The population consists of 100 genomes.

2.  Each genome is a crossword puzzle consisting of all the words

3.  We get the 8 best genomes of the population

4.  Crossover all the best genomes in pairs

5.  Adding all genomes from the previous population to the new
    population

6.  Mutating all genomes

7.  Crossover - takes two parents and returns only one child

8.  Maximum number of populations is equal to 20000

The main function is also configured to read test input data with words
and crossword generation, and it is possible to output a crossword.grid
for a visual understanding of what a crossword puzzle looks like

    def select_best_genomes(population, num_best):
        # ...

    def main():
        # ...
