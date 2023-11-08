import spacy
import random
import rules

nlp = spacy.load("en_core_web_sm")

POPULATION_SIZE = 10

def generate_individual(words):
    doc = nlp(words)
    tokens = [token.text for token in doc]
    random.shuffle(tokens)
    return ' '.join(tokens)

def cal_fitness(words):
    score = 0
    doc = nlp(words)
    subj_position = []
    verb_position = []
    obj_position = []
    amod_position = -1
    
    for i, token in enumerate(doc):
        # print(token.text, token.dep_)
        if "nsubj" in token.dep_:
            subj_position.append(i)
            score += 1
        elif "ROOT" in token.dep_:
            verb_position.append(i)
            score += 1
        elif "amod" in token.dep_:
            amod_position = i
            score += 1
        elif "obj" in token.dep_:
            obj_position.append(i)
            score += 1
    if(len(subj_position) == 0 or len(verb_position) == 0 or len(obj_position) == 0):
        return score
    if len(subj_position) > 1 or len(verb_position) > 1 or len(obj_position) > 1:
        return -1
    if(subj_position[0] == 0):
        score += 1
    if(amod_position == -1):
        if subj_position[0] < verb_position[0] < obj_position[0]:
            score += 1
    else:
        if(subj_position[0] < verb_position[0] < amod_position < obj_position[0]):
            score += 1

    return score

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

def main():
    words = input('Nhập các từ: ')
    count = 0
    for token in nlp(words):
        count += 1
    if(count < 3 or count > 5):
        print('Xin lỗi vì sự bất tiện này, hệ thống chỉ hoạt động khi số lượng từ lớn hơn 3 và nhỏ hơn 5.')
        return
    
    global POPULATION_SIZE

    generation = 1
    population = set()
    for i in range(POPULATION_SIZE):
        individual = generate_individual(words)
        population.add(individual)

    population = list(population)
    
    found = False

    # Rank Selection
    population = sorted(population, key = lambda x:cal_fitness(x), reverse=True)
    totalScore = 0
    for individual in population:
        totalScore += cal_fitness(individual)

    weights = []
    parents = set()
    for individual in population:
        weights.append(cal_fitness(individual) / totalScore)
    
    while len(parents) < 4:
        parent = random.choices(population, weights=weights, k=1)[0]
        parents.add(parent)
    
    parents = list(parents)

    for i in range(len(parents)):
        parents[i] = parents[i].split()
 

    # Lai ghép Order-1
    children = []
    for i in range(len(parents) - 1):
        for j in range(i + 1, len(parents)):
            parent1 = parents[i]
            parent2 = parents[j]
            child1 = order_crossover(parent1, parent2)
            child2 = order_crossover(parent2, parent1)
            children.append(child1)
            children.append(child2)
    
    # print(children)

    # Đột biến hoán vị phép trộn
    mutations = []
    for i in range(len(children)):
        index = random.sample(range(len(children[0]) - 1), 1)[0]
        slice_child1 = sorted(children[i][0:index], reverse=True)
        slice_child2 = children[i][index:]
        mutation = slice_child1 + slice_child2
        mutation = " ".join(mutation)
        mutations.append(mutation)
    
    print('Những gene tốt nhất:')
    for gene in mutations:
        if(cal_fitness(gene) == 5):
            print(gene)


    
    

    

    # print(cal_fitness(words))
   

    
if __name__ == '__main__': 
    main()     