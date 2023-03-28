import random
import matplotlib.pyplot as plt

def view(board):
    for i in range(8):
        for j in range(8):
            if board[i] == j:
                print('[R]', end=' ')
            else:
                print('[ ]', end=' ')
        print()

def fitness(board):
    attacks = 0
    for i in range(len(board)-1):
        for j in range(i + 1, len(board)-1):
            if board[i] == board[j]:
                attacks += 1
    for i in range(len(board)-1):
        for j in range(i + 1, len(board)-1):
            if abs(board[j] - board[i]) == abs(j - i):
                attacks += 1
    return 28 - attacks

def crossover(board1, board2, crossover_rate): #Crossover variado
    if random.random() < crossover_rate:
        split_point = random.randint(1, 7)
        new_board1 = board1[:split_point] + board2[split_point:]
        new_board2 = board2[:split_point] + board1[split_point:]
        return new_board1, new_board2
    else:
        return board1, board2

def mutate(board, mutation_rate): #Mutação Variada
    boardCopy = board.copy()
    if random.random() < mutation_rate:
        index = random.randint(0, 7)
        new_value = random.randint(0, 7)
        boardCopy[index] = new_value
    return boardCopy

def diversity(population):
    diversity = 0
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            if population[i] != population[j]:
                diversity += 1
    return diversity


def calibrate_rates(population_diversity, mutation_rate, crossover_rate):

    if population_diversity > population_size * 0.7:
        crossover_rate = crossover_rate + (crossover_rate * 0.1)
        mutation_rate = mutation_rate - (mutation_rate * 0.1)
    else:
        crossover_rate = crossover_rate - (crossover_rate * 0.1)
        mutation_rate = mutation_rate + (mutation_rate * 0.1)

    return crossover_rate, mutation_rate

population_size = 100
crossover_rate = 0.6
mutation_rate = 0.1
generations = 75

population = []
for i in range(population_size):
    board = [random.randint(0, 7) for j in range(8)]
    population.append(board)

max_fitness = []

for generation in range(generations):
    fitness_scores = [fitness(board) for board in population]
    max_fitness.append(max(fitness_scores))
    
    parents = []
    for i in range(population_size):
        p1 = random.randint(0, population_size-1)
        p2 = random.randint(0, population_size-1)
        if fitness_scores[p1] > fitness_scores[p2]:
            parents.append(population[p1])
        else:
            parents.append(population[p2])
    
    new_population = []
    for i in range(int(population_size/2)):
        p1 = i * 2
        p2 = i * 2 + 1
        
        population_diversity = diversity(population)

        crossover_rate, mutation_rate = calibrate_rates(population_diversity, mutation_rate, crossover_rate)

        offspring1, offspring2 = crossover(parents[p1], parents[p2], crossover_rate)
        offspring1 = mutate(offspring1, mutation_rate)
        offspring2 = mutate(offspring2, mutation_rate)
        new_population.append(offspring1)
        new_population.append(offspring2)

    population = new_population

best_board = max(population, key=fitness)
print('Melhor solução:')
view(best_board)

plt.plot(range(generations), max_fitness, color='red')
plt.title("Maior fitness por geração com taxas variadas")
plt.ylabel("Fitness")
plt.xlabel("Geração")
plt.show()
