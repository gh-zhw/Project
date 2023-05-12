import random


def random_split(data, p):
    if 1-sum(p) > 1e-3:
        raise ValueError("Sum of p isn't 1!")

    data_num = len(data)
    random.shuffle(data)

    if len(p) == 2:
        part1 = data[:int(data_num * p[0])]
        part2 = data[int(data_num * p[0]):]
        return part1, part2
    elif len(p) == 3:
        part1 = data[:int(data_num * p[0])]
        part2 = data[int(data_num * p[0]):int(data_num * (p[0] + p[1]))]
        part3 = data[int(data_num * (p[0] + p[1])):]
        return part1, part2, part3


if __name__ == '__main__':
    data = [i for i in range(80)]
    # part1, part2, part3 = random_split(data, [0.7, 0.2, 0.1])
    # print(len(part1))
    # print(len(part2))
    # print(len(part3))

    part1, part2 = random_split(data, [0.7, 0.3])
    print(len(part1))
    print(len(part2))
