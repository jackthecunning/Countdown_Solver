import itertools
from multiprocessing import Manager
from multiprocessing import Pool
import os
import random
import string

import enchant

d = enchant.Dict('en_US')


def get_components():
    print("Please enter each number or letter seperated by a space")
    print("If this is a Numbers game submit answer last")

    comps = input().split(' ')
    numbers = []
    letters = []
    for comp in comps:
        if comp.isnumeric():
            numbers.append(int(comp))
        if len(comp) == 1:
            letters.append(comp)

    if len(numbers) == 7 and len(letters) == 0:
        return "numbers_game", numbers
    elif len(letters) == 9 and len(numbers) == 0:
        return "letters_game", letters
    else:
        print("Since you couldn't follow the rules we'll play a random game.")
        return "random", ['a']


def gen_rand_numbers(small, big):
    answer = random.randint(100, 999)

    numbers = []
    for j in range(big):
        numbers.append(random.randint(1, 4) * 25)
    for i in range(small):
        numbers.append(random.randint(1, 9))

    return answer, numbers


def do_math(total, x2, math_function):
    if math_function == "add":  # add
        return total + x2
    if math_function == "subtract":  # subtract
        return total - x2
    if math_function == "multiply":  # multiply
        return total * x2
    if math_function == "divide":  # divide
        return total / x2


def numbers_game(numbers, answer):
    # x = [1, 2, 3, 4]
    math_functions = ["add", "subtract", "multiply", "divide"]
    figs = {"add": '+', "subtract": '-', "multiply": 'x', "divide": '/'}
    sol = ""

    min_err = answer
    closest_val = 0
    min_p = ()
    min_q = ()

    # create permutations for sets between 2 and 6 numbers in size
    for i in range(2, 7):
        for perm in itertools.permutations(numbers, i):

            # try different math function between each pair of numbers
            for qs in itertools.product(math_functions, repeat=i - 1):
                total = perm[0]

                # Apply math to generate total
                for s in range(len(qs)):
                    total = do_math(total, perm[s + 1], qs[s])
                    if float(total).is_integer() is False:
                        # You can't play with fractions in Countdown
                        break

                # Update how close to the answer we are getting
                if abs(total - answer) < min_err:
                    min_err = abs(total - answer)
                    closest_val = total
                    min_p = perm
                    min_q = qs

                # Finally, we've found a matching solution
                if total == answer:
                    for i in range(len(qs)):
                        sol = sol + str(perm[i]) + " "
                        sol = sol + figs[qs[i]] + " "
                    sol = sol + str(perm[len(perm) - 1])
                    return total, sol

    for i in range(len(min_q)):
        sol = sol + str(min_p[i]) + " "
        sol = sol + figs[min_q[i]] + " "
    sol = sol + str(min_p[len(min_p) - 1])
    return closest_val, sol


def play_numbers_game(numbers=[]):
    if len(numbers) > 0:
        answer = numbers.pop()

    else:
        answer, numbers = gen_rand_numbers(4, 2)
    total, solution = numbers_game(numbers, answer)

    print('\n')
    print(f"We played the Numbers game attempting to solve for {answer}.")
    print(f"We started with numbers {numbers}")
    print(f"Our answer of {total} is {abs(answer - int(total))} away.")
    print(solution)
    print(f"Thats good for {10 - (abs(answer - int(total)))} points!")


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

    # Order our list of solutions. Our longest solution will be first in line.
    solutions = sorted(list(dict.fromkeys(solutions)), key=len, reverse=True)
    return solutions


def play_letters_game():
    letters = gen_rand_letters(5, 4)
    answers = letters_game(letters)

    answer = answers[0]
    if len(answer) == 9:
        score = 18
    else:
        score = len(answer)

    print('\n')
    print("*** Letters Game ***")
    print(f"We were given the letters {letters}")
    print(f"We found {len(answer)} letter word {answer}")
    print(f"Thats good for {score} points!")


def main():
    game, components = get_components()
    if game == "numbers_game":
        play_numbers_game(components)
    elif game == "letters_game":
        play_letters_game(components)
    else:
        play_numbers_game()
        play_letters_game()


if __name__ == '__main__':
    main()
