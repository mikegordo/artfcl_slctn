import random
import os
from comparator import string_similarity

MUTATION_PROBABILITY = os.environ.get('MUTATION_PROBABILITY', 3)

def incubate(current: str, target: str, count: int) -> dict:
    result = {
        "keys": [],
        "mapping": {},
        "best": 0
    }

    for i in range(count):
        n = random.randint(1, MUTATION_PROBABILITY)
        val = current
        for k in range(n):
            val = change_char(val)
        j = string_similarity(target, val)
        result['best'] = max(result['best'], j)
        result['keys'].append(val)
        result['mapping'][j] = val
    return result

def change_char(current: str) -> str:
    index = random.randint(0, len(current)-1)
    new_char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
    return current[:index] + new_char + current[index+1:]
