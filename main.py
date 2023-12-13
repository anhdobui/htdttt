import spacy
import random
import rules
from itertools import permutations

nlp = spacy.load("en_core_web_sm")

POPULATION_SIZE = 10

class BreakOut(Exception):
    pass
def print_result_generation(gen_th,population):
    print(f"Thế hệ F {gen_th}: {fitness_average(population)}")
    for i in range(len(population)):
        print(f"Cá thể {i}: {population[i]} ---fitness--- {cal_fitness(population[i])}")
        
def generate_individual(words):
    doc = nlp(words)
    tokens = [token.text for token in doc]
    random.shuffle(tokens)
    return ' '.join(tokens)

def cal_fitness(words):
    return rules.compare_struct(words)

def order_crossover(parent1, parent2):
    # Chọn hai điểm cắt ngẫu nhiên
    length = len(parent1)
    cut1, cut2 = random.sample(range(length), 2)
    cut1, cut2 = min(cut1, cut2), max(cut1, cut2)

    # Sao chép phần đoạn giữa cut1 và cut2 từ parent1 vào chromosome con
    child = [None] * length
    child[cut1:cut2] = parent1[cut1:cut2]

    # Sao chép các gen còn lại từ parent2 vào chromosome con
    for gene in parent2:
        if gene not in child:
            for i in range(length):
                if child[i] is None:
                    child[i] = gene
                    break
    return child

def generate_children(parents):
    for i in range(len(parents)):
        parents[i] = parents[i].split()

    children = []
    for i in range(0, len(parents) - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        child1 = order_crossover(parent1, parent2)
        child2 = order_crossover(parent2, parent1)
        children.append(child1)
        children.append(child2)

    return children

def convert_to_string(arr):
    for i in range(len(arr)):
        arr[i] = " ".join(arr[i])
    return arr  

def rank_selection(population, number):
    ranked_solutions = sorted(population, key = lambda x:cal_fitness(x), reverse=True)
    totalScore = 0
    for individual in ranked_solutions:
        totalScore += cal_fitness(individual)

    weights = []
    parents = []
    for individual in ranked_solutions:
        weights.append(cal_fitness(individual) / totalScore)
    
    while len(parents) < number:
        parent = random.choices(ranked_solutions, weights=weights, k=1)[0]
        parents.append(parent)
    return parents

def fitness_average(arr):
    sum = 0
    for item in arr:
        sum += cal_fitness(item)
    return sum/len(arr)
def genetic_algorithm(population):
    generation = 1
    mutations = []
    print_result_generation(generation-1,population)
    try:
        while generation < 100:
            mutations = []
            # Rank Selection and Steady State selection
            parents = rank_selection(population, 6)
            parents_copy = parents.copy()
            # Lai ghép Order-1
            children = generate_children(parents_copy)
            children_clone = convert_to_string(children)
            res = rank_selection(children_clone, 4)
            result = parents + res
            # Lai ghép Order-1
            children_2 = generate_children(result)
            
            # Đột biến hoán vị phép trộn
            children_random = random.randint(0, 9)
            index1, index2 = random.sample(range(len(children_2[children_random])), 2)
            children_2[children_random][index1], children_2[children_random][index2] = children_2[children_random][index2], children_2[children_random][index1]
            
            for children_2_item in children_2:
                mutation = " ".join(children_2_item)
                mutations.append(mutation)
        
            # In kết quả
            print_result_generation(generation,mutations)
            
            # Tạo điều kiện dừng sớm
            for item in mutations:
                fitness_item = cal_fitness(item)
                if(fitness_item == 1):
                    raise BreakOut
            generation += 1
    except BreakOut:
        pass
    
    arranged = ''
    fitness_max = 0
    for mutation in mutations:
        fitness_mutation = cal_fitness(mutation)
        if(fitness_mutation > fitness_max):
            arranged = mutation
            fitness_max = fitness_mutation
    print("------------------------------------------")
    print("Kết quả câu sau khi sắp xếp là: "+arranged)
    
def main():
    words = input('Nhập các từ: ')    
    count = 0
    for _ in nlp(words):
        count += 1
    if count <= 3:
        words = words.split()
        word_permutations = permutations(words)
        for perm in word_permutations:
            if(cal_fitness(' '.join(perm)) == 1):
                print("Kết quả câu sau khi sắp xếp là: ", ' '.join(perm))
        return
    if(count > 6):
        print('Hệ thống chỉ hoạt động tốt khi số lượng nhỏ hơn 5.')
        return
    global POPULATION_SIZE
    population = []
    for i in range(POPULATION_SIZE):
        individual = generate_individual(words)
        population.append(individual)
        
    genetic_algorithm(population)
    
        
if __name__ == '__main__': 
    main()     