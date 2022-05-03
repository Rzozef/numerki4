# dodac funkcje ktore beda dzialac i dla kontrastu te ktore nie beda (nie mają pochodnej, czy cos)
# -M <= |f(x)| <= M  ##### jakis wazny warunek
# funckje wymierne nadają sie do przykladow negatywnych
# trzymaj sie instrukcji bo cie Runge zmiecie z planszy
# uruchomic pare razy, wyniki sie powinny powtarzac
# TODO zlozona kwadratura newtona-cotesa oparta na trzech wezlach (wzor simpsona), gauss-czebyszew

import math
import matplotlib.pyplot as pyplot
import numpy as np

from math import sin, sqrt


def draw_function(function, a, b):
    a = min(math.floor(a), math.ceil(a))
    b = max(math.floor(b), math.ceil(b))
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

    pyplot.xticks(np.arange(min(x), max(x) + 1, 1.0))
    pyplot.legend()
    pyplot.show()


class Function:
    def __init__(self, calc):
        self.__calc = calc

    def __call__(self, x):
        return self.__calc(x)


def simpson(f, a, b, e):
    prev_val = None
    curr_val = None
    intervals = 3  # musi być >= 2 i nieparzysta

    while prev_val is None or abs(prev_val - curr_val) >= e:
        prev_val = curr_val
        h = (b - a) / intervals
        sum = f(a) + f(b)

        for i in range(1, intervals):
            if i % 2 == 1:
                sum += 4 * f(a + i * h)
            else:
                sum += 2 * f(a + i * h)

        sum *= h
        sum /= 3

        curr_val = sum
        intervals *= 2
    return curr_val


# do porównania newtona_cotesa z naszą metodą musimy obliczyc granice
# nie wiem czy to jest dobrze, ta instrukcja jest zjebana
# przypomnij zeby pousuwac komentarze przed oddaniem xd
def simpson_limit(func, epsilon: float) -> float:
    a = 0
    b = 0.5
    result = 0
    # granica do +1
    while True:
        integral = simpson(func, a, b, epsilon)
        result += integral
        a = b
        b = b + (1 - b) / 2
        if abs(integral) < epsilon:
            break
    # granica do -1
    a = -0.5
    b = 0
    while True:
        integral = simpson(func, a, b, epsilon)
        result += integral
        b = a
        a = a - (1 - abs(a)) / 2
        if abs(integral) < epsilon:
            break
    return result


def main():
    functions = [
        ("x^2 + 2", Function(lambda x: x ** 2 + 2)),
        ("sin(x)", Function(lambda x: sin(x))),
        ("x^5 + 3x^4 + x^2 + 1", Function(lambda x: x ** 5 + 3 * x ** 4 + x ** 2 + 1)),
        ("1 / (2 * sqrt(x))", Function(lambda x: 1 / 2 * sqrt(x)))
    ]

    function_choice = None
    e = 0

    while function_choice is None:
        print("Wybierz funkcje")
        for i in range(len(functions)):
            print(f"\t{i + 1}. {functions[i][0]}")
        function_choice = input("\t>>>>")
        if int(function_choice) not in range(1, len(functions) + 1):
            print("Nie ma takiej opcji w menu")
            function_choice = None
    print("Podaj dolny przedział funkcji")
    a = input("\t>>>>")
    b = a
    while float(b) <= float(a):
        print("Podaj górny przedział funkcji")
        b = input("\t>>>>")
    while float(e) <= 0:
        print("Podaj dokladnosc")
        e = input("\t>>>>")
    chosen_function = functions[int(function_choice) - 1][1]
    print(simpson(chosen_function, float(a), float(b), float(e)))
    #draw_function(chosen_function, float(a), float(b))


if __name__ == '__main__':
    main()
