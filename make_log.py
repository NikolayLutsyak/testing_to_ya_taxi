import numpy as np

def main(number_of_lines):
    types = ['/index', '/test', '/home']
    with open('log.txt', 'w') as file:
        for i in range(number_of_lines):
            file.write('{},{},{}\n'.format(
                i, types[np.random.randint(0, 3)], np.random.binomial(1, 0.3)))

if __name__ == '__main__':
    main(1000000)
