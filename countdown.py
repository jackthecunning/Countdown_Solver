import itertools
from multiprocessing import Manager
from multiprocessing import Pool
import os
import random
import string

import enchant

d = enchant.Dict('en_US')

# Numbers game


def gen_rand_numbers(small, big):
    answer = random.randint(100, 999)
    print(answer)

    numbers = []
    for j in range(big):
        numbers.append(random.randint(1, 4) * 25)
    for i in range(small):
        numbers.append(random.randint(1, 9))
    print(numbers)

    return answer, numbers


def do_math(x1, x2, f):
    if f == 1:  # add
        return x1 + x2
    if f == 2:  # subtract
        return x1 - x2
    if f == 3:  # multiply
        return x1 * x2
    if f == 4:  # divide
        return x1 / x2


def numbers_game(numbers, answer):
    x = [1, 2, 3, 4]
    figs = {1: '+', 2: '-', 3: 'x', 4: '/'}
    sol = ""

    min_err = answer
    closest_val = 0
    min_p = ()
    min_q = ()

    # create permutations for sets between 2 and 6 numbers in size
    for i in range(2, 7):
        for ps in itertools.permutations(numbers, i):
            for qs in itertools.product(x, repeat=i - 1):
                total = ps[0]

                for s in range(len(qs)):
                    total = do_math(total, ps[s + 1], qs[s])
                    if float(total).is_integer() is False:
                        break

                if abs(total - answer) < min_err:
                    min_err = abs(total - answer)
                    # min_err = total
                    closest_val = total
                    min_p = ps
                    min_q = qs

                if total == answer:
                    for i in range(len(qs)):
                        sol = sol + str(ps[i]) + " "
                        sol = sol + figs[qs[i]] + " "
                    sol = sol + str(ps[len(ps) - 1])
                    return total, sol

    for i in range(len(min_q)):
        sol = sol + str(min_p[i]) + " "
        sol = sol + figs[min_q[i]] + " "
    sol = sol + str(min_p[len(min_p) - 1])
    return closest_val, sol


def play_numbers_game():
    answer, numbers = gen_rand_numbers(4, 2)
    total, solution = numbers_game(numbers, answer)
    print(int(total), solution)
    print(abs(answer - int(total)), '\n')


def gen_rand_letters(cons, vows):
    vowels = ['a', 'e', 'i', 'o', 'u']
    letters = ""

    for i in range(cons):
        letter = 'a'
        while letter in vowels:  # keep going til get consenant
            letter = random.choice(string.ascii_letters).lower()
        letters += letter
    for i in range(vows):
        letter = 'b'
        while letter not in vowels:  # keep going til get vowel
            letter = random.choice(string.ascii_letters).lower()
        letters += letter
    return letters


def check_words(word):
    if d.check(word) is True:
        solutions.append(word)


def letters_game(letters):
    counter = 0
    words = []
    for i in range(9, 1, -1):
        for p in itertools.permutations(letters, i):
            counter += 1
            word = ''.join(p)
            words.append(word)

    # multiprocessing helps us check all possible words
    manager = Manager()
    global solutions
    solutions = manager.list()
    pool = Pool(processes=os.cpu_count())
    pool.map(check_words, words)
    pool.close()
    pool.join()

    solutions = sorted(list(dict.fromkeys(solutions)), key=len, reverse=True)
    return solutions


def play_letters_game():
    letters = gen_rand_letters(5, 4)
    answers = letters_game(letters)
    print(letters)
    print(answers)


def main():
    play_numbers_game()
    play_letters_game()


if __name__ == '__main__':
    main()
