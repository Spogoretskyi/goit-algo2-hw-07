import timeit
import matplotlib.pyplot as plt
from functools import lru_cache
from splay_tree import SplayTree


# Реалізація Fibonacci з використанням LRU-кешу
@lru_cache(maxsize=1000)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay(n, tree):
    result = tree.find(n)
    if result is not None:
        return result

    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


def measure_lru_time(n):
    return fibonacci_lru(n)


def measure_splay_time(n):
    tree = SplayTree()
    return fibonacci_splay(n, tree)


if __name__ == "__main__":
    n_values = range(0, 951, 50)
    lru_times = []
    splay_times = []

    for n in n_values:
        lru_time = timeit.timeit(lambda: measure_lru_time(n), number=10)
        splay_time = timeit.timeit(lambda: measure_splay_time(n), number=10)
        lru_times.append(lru_time)
        splay_times.append(splay_time)

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, lru_times, label="LRU Cache", marker="o")
    plt.plot(n_values, splay_times, label="Splay Tree", marker="s")
    plt.xlabel("n (Fibonacci index)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.title("Порівняння часу виконання для LRU Cache vs Splay Tree")
    plt.legend()
    plt.grid()
    plt.show()

    # Таблиця результатів
    print("n\tLRU Cache Time (s)\tSplay Tree Time (s)")
    print("-" * 50)
    for n, lru_time, splay_time in zip(n_values, lru_times, splay_times):
        print(f"{n}\t{lru_time:.8f}\t{splay_time:.8f}")
