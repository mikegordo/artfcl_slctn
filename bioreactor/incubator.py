import random
from comparator import string_similarity

def incubate(current: str, target: str, count: int, mutation_probability: int) -> dict:
    result = {
        "keys": [],
        "mapping": {},
        "best": 0
    }

    for i in range(count):
        n = random.randint(1, mutation_probability)
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
