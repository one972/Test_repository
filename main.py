import numpy as np
import matplotlib.pyplot as plt

class TravelingSalesman: #класс коммивояжёра
    def __init__(self, num_cities, min_coord, max_coord):
        self.num_cities = num_cities
        self.min_coord = min_coord
        self.max_coord = max_coord
        self.X = np.random.uniform(min_coord, max_coord, num_cities)
        self.Y = np.random.uniform(min_coord, max_coord, num_cities)
        self.S = np.arange(num_cities)
        np.random.shuffle(self.S)

    def calculate_distance(self, order): #ф-ия подсчета дистанции
        total_distance = 0
        for i in range(len(order) - 1):
            total_distance += np.sqrt((self.X[order[i+1]] - self.X[order[i]])**2 + (self.Y[order[i+1]] - self.Y[order[i]])**2)
        total_distance += np.sqrt((self.X[order[0]] - self.X[order[-1]])**2 + (self.Y[order[0]] - self.Y[order[-1]])**2) #дистанция между первым и последним городом
        return total_distance

    def swap_cities(self, order):
        new_order = order.copy() #копия текущего порядка
        idx1, idx2 = np.random.choice(len(order)-1, 2, replace=False) #выбор двух случайных городов
        new_order[idx1:idx2+1] = np.flipud(new_order[idx1:idx2+1]) #смена местами
        return new_order

    def cool_down(self, t_max, k):
        return 0.1 * t_max / k #охлаждение

    def acceptance_probability(self, e_cur, e_next, t):
        return np.exp((e_cur - e_next) / t) #шанс перехода в новое состояние

    def minimize_path(self, t_max, t_min, k_max):
        t = t_max #начальная температура
        e_cur = self.calculate_distance(self.S) #начальная дистанция
        k = 1
        while t > t_min and k < k_max:
            S_new = self.swap_cities(self.S) #новый путь
            e_new = self.calculate_distance(S_new) #новая длина пути
            if e_new <= e_cur or np.random.rand() <= self.acceptance_probability(e_cur, e_new, t): #либо идем вниз либо вверх с шансом 
                self.S = S_new
                e_cur = e_new #замена пути
            t = self.cool_down(t_max, k) #охлаждение
            k += 1
        return e_cur, k, self.S

    def plot_path(self, order):
        plt.plot(self.X[order], self.Y[order], '-*')
        plt.title(f"Total Distance: {self.calculate_distance(order):.6f}")
        plt.show()

if __name__ == "__main__":
    num_cities = 20
    min_coord, max_coord = 0, 10
    t_max = 1000
    t_min = 0.001
    k_max = 1000000

    salesman = TravelingSalesman(num_cities, min_coord, max_coord) #создание класса коммивояжёра
    print(f"Initial Order: {salesman.S}\nInitial Distance: {salesman.calculate_distance(salesman.S):.6f}")

    for i in range(3):
        total_distance, iterations, optimal_order = salesman.minimize_path(t_max, t_min, k_max)
        print(f"Iteration {i+1} - Total Distance: {total_distance:.6f}, Iterations: {iterations}, Optimal order: {optimal_order}")
        salesman.plot_path(optimal_order)
