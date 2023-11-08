import random

def ordered_crossover(parent1, parent2):
    # Chọn hai điểm cắt ngẫu nhiên
    length = len(parent1)
    cut1, cut2 = random.sample(range(length), 2)
    cut1, cut2 = min(cut1, cut2), max(cut1, cut2)
    print(cut1, cut2)

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

# Ví dụ
parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
parent2 = [9, 3, 7, 8, 2, 6, 5, 1, 4]
child = ordered_crossover(parent1, parent2)
print(child)