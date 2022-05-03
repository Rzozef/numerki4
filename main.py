# dodac funkcje ktore beda dzialac i dla kontrastu te ktore nie beda (nie mają pochodnej, czy cos)
# funckje wymierne nadają sie do przykladow negatywnych
# trzymaj sie instrukcji bo cie Runge zmiecie z planszy
# uruchomic pare razy, wyniki sie powinny powtarzac

import math
import matplotlib.pyplot as pyplot
import numpy as np

from math import cos, pi, sin, sqrt


def draw_function(function, a, b, nodes=[]):
    x = np.linspace(a, b, 100)

    figure = pyplot.figure()
    axis = figure.add_subplot(1, 1, 1)
    axis.spines['right'].set_color('none')
    axis.spines['top'].set_color('none')
    axis.xaxis.set_ticks_position('bottom')
    axis.spines['bottom'].set_position(('data', 0))
    axis.yaxis.set_ticks_position('left')
    axis.spines['left'].set_position(('data', 0))

    axis.plot(1, 0, ls="", marker=">", ms=10, color="k",
              transform=axis.get_yaxis_transform(), clip_on=False)
    axis.plot(0, 1, ls="", marker="^", ms=10, color="k",
              transform=axis.get_xaxis_transform(), clip_on=False)

    y_vals = x.copy()
    for i in range(len(y_vals)):
        y_vals[i] = function(x[i])
    pyplot.plot(x, y_vals, 'r', label="f(x)")

    section = np.arange(a, b, 0.0001)
    y_vals = section.copy()
    for i, val in enumerate(y_vals):
        y_vals[i] = function(val)
    pyplot.fill_between(section, y_vals, color='b', alpha=.2)

    for i, node_x in enumerate(nodes):
        node_y = function(node_x)
        pyplot.plot(node_x, node_y, 'rx')

    pyplot.axvline(x=a)
    pyplot.axvline(x=b)

    pyplot.xticks(np.arange(min(x), max(x) + 1, 1.0))
    pyplot.legend()
    pyplot.show()


class Function:
    def __init__(self, calc):
        self.__calc = calc

    def __call__(self, x):
        return self.__calc(x)


def simpson(f, a, b, e, wage_function):
    prev_val = None
    curr_val = None
    nodes = 3  # musi być >= 2 i nieparzysta

    while prev_val is None or abs(prev_val - curr_val) >= e:
        prev_val = curr_val
        h = (b - a) / nodes
        sum = f(a) * wage_function(a)
        sum += f(b) * wage_function(b)

        for i in range(1, nodes + 1):
            if i % 2 == 1:
                sum += 4 * f(a + i * h) * wage_function(a + i * h)
            else:
                sum += 2 * f(a + i * h) * wage_function(a + i * h)

        sum *= h
        sum /= 3

        curr_val = sum
        nodes += 2
    return curr_val, nodes


def gauss_czebyszew(f, n):
    sum = 0
    A = pi / (n + 1)
    nodes = []
    for i in range(0, n + 1):
        x = cos(((2 * i + 1) * pi) / (2 * n + 2))
        nodes.append(x)
        sum += A * f(x)
    return sum, nodes


def simpson_limit(func, epsilon: float, wage_function) -> float:
    a = 0
    b = 0.5
    result = 0
    # granica do +1
    while True:
        integral = simpson(func, a, b, epsilon, wage_function)[0]
        result += integral
        a = b
        b = b + (1 - b) / 2
        if abs(integral) < epsilon:
            break
    # granica do -1
    a = -0.5
    b = 0
    while True:
        integral = simpson(func, a, b, epsilon, wage_function)[0]
        result += integral
        b = a
        a = a - (1 - abs(a)) / 2
        if abs(integral) < epsilon:
            break
    return result


def main():
    functions = [
        ("1", Function(lambda x: 1)),
        ("x^2 + 2", Function(lambda x: x ** 2 + 2)),
        ("sin(x)", Function(lambda x: sin(x))),
        ("x^5 + 3x^4 + x^2 + 1", Function(lambda x: x ** 5 + 3 * x ** 4 + x ** 2 + 1)),
        ("1 +  1 / (1 + 25x^2)", Function(lambda x: 1 + 1 / (1 + 25 * x**2))),
        ("|1 / x|", Function(lambda x: abs(1 / x))),
        ("1 / sqrt(1 - x^2)", Function(lambda x: 1 / sqrt(1 - x**2)))
    ]

    function_choice = None
    method_choice = None
    e = 0
    calc_limit = None
    nodes = []

    while function_choice is None:
        print("Wybierz funkcje")
        for i in range(len(functions)):
            print(f"\t{i + 1}. {functions[i][0]}")
        function_choice = input("\t>>>>")
        if int(function_choice) not in range(1, len(functions) + 1):
            print("Nie ma takiej opcji w menu")
            function_choice = None
    chosen_function = functions[int(function_choice) - 1][1]
    while method_choice is None:
        print("Wybierz metode")
        print("\t1. Newton-Cotes")
        print("\t2. Gauss-Czebyszew")
        method_choice = input("\t>>>>")
        if int(method_choice) not in range(1, 3):
            print("Nie ma takiej opcji w menu")
            method_choice = None
    if int(method_choice) == 1:
        wage_function = None
        while wage_function is None:
            print("Wybierz funkcję wagową:")
            for i in range(len(functions)):
                print(f"\t{i + 1}. {functions[i][0]}")
            wage_function = input("\t>>>>")
            if int(function_choice) not in range(1, len(functions) + 1):
                print("Nie ma takiej opcji w menu")
                wage_function = None
        wage_function = functions[int(wage_function) - 1][1]
        print("Podaj dolny przedział funkcji")
        a = input("\t>>>>")
        b = a
        while float(b) <= float(a):
            print("Podaj górny przedział funkcji")
            b = input("\t>>>>")
        while float(e) <= 0:
            print("Podaj dokladnosc")
            e = input("\t>>>>")
        while calc_limit is None:
            print("Liczyc granice funkcji na przedziale")
            print("\t1. Tak")
            print("\t2. Nie")
            calc_limit = input("\t>>>>")
        if calc_limit == "2":
            result = simpson(chosen_function, float(a), float(b), float(e), wage_function)
            print(result[0])
            print(result[1])
            nodes = np.arange(float(a), float(b), (float(b) - float(a)) / result[1])
            draw_function(chosen_function, float(a), float(b), nodes)
        else:
            print(simpson_limit(chosen_function, float(e), wage_function))
    else:
        a, b = -0.99, 0.99
        for n in range(2, 6):
            result = gauss_czebyszew(chosen_function, n)
            print(f"Wynik dla {n} węzłów: {result[0]}")
            nodes = result[1]
            draw_function(Function(lambda x: chosen_function(x) / sqrt(1 - x ** 2)), float(a), float(b), nodes)


if __name__ == '__main__':
    main()
