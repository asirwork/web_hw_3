from multiprocessing import Pool, cpu_count
from time import time


def factorize(*args):
    result = []
    for number in args:
        divisors = []
        for i in range(1, number + 1):
            if number % i == 0:
                divisors.append(i)
        result.append(divisors)
    return result


if __name__ == '__main__':
    numbers = (128, 255, 99999, 10651060)
    print("Реалізація синхронного виконання коду:")
    start_time_1 = time()
    factorize(*numbers)
    end_time_1 = time()
    total_time_1 = end_time_1 - start_time_1
    print(f"Час виконання: {round(total_time_1, 2)}")
    print("-----------------------------------------------------------------")
    total_cpu = cpu_count()
    print(f"Реалізація паралельного обчислення з використанням {total_cpu} ядер процесора:")
    start_time_2 = time()
    with Pool(processes=total_cpu) as pool:
        pool.map(factorize, numbers)
    end_time_2 = time()
    total_time_2 = end_time_2 - start_time_2
    print(f"Час виконання: {round(total_time_2, 2)}")
    print("-----------------------------------------------------------------")