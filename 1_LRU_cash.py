import random
import time
from functools import lru_cache


# Функція для обчислення суми без кешу
def range_sum_no_cache(array, L, R):
    return sum(array[L : R + 1])


# Функція для оновлення масиву без кешу
def update_no_cache(array, index, value):
    array[index] = value


@lru_cache(maxsize=1000)
def cached_range_sum(array_id, L, R):
    global array_store
    array = array_store[array_id]
    return sum(array[L : R + 1])


def range_sum_with_cache(array, L, R):
    return cached_range_sum(id(array), L, R)


def update_with_cache(array, index, value):
    global cached_range_sum
    array[index] = value
    cached_range_sum.cache_clear()


if __name__ == "__main__":
    N = 100000
    Q = 50000
    array = [random.randint(1, N) for _ in range(N)]
    queries = [
        (
            random.choice(["Range", "Update"]),
            random.randint(0, N - 1),
            random.randint(0, N - 1),
        )
        for _ in range(Q)
    ]

    for i, query in enumerate(queries):
        if query[0] == "Range" and query[1] > query[2]:
            queries[i] = ("Range", query[2], query[1])

    array_store = {id(array): array}

    # Тестування виконання без кешу
    start_time_no_cache = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array, query[1], query[2])
        elif query[0] == "Update":
            update_no_cache(array, query[1], query[2])
    end_time_no_cache = time.time()

    # Тестування виконання з кешем
    start_time_with_cache = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array, query[1], query[2])
        elif query[0] == "Update":
            update_with_cache(array, query[1], query[2])
    end_time_with_cache = time.time()

    print(
        f"Час виконання без кешування: {end_time_no_cache - start_time_no_cache:.2f} секунд"
    )
    print(
        f"Час виконання з LRU-кешем: {end_time_with_cache - start_time_with_cache:.2f} секунд"
    )
