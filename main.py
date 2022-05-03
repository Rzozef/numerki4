# dodac funkcje ktore beda dzialac i dla kontrastu te ktore nie beda (nie mają pochodnej, czy cos)
# -M <= |f(x)| <= M  ##### jakis wazny warunek
# funckje wymierne nadają sie do przykladow negatywnych
# trzymaj sie instrukcji bo cie Runge zmiecie z planszy
# uruchomic pare razy, wyniki sie powinny powtarzac
# TODO zlozona kwadratura newtona-cotesa oparta na trzech wezlach (wzor simpsona), gauss-czebyszew
from math import sin, sqrt


class Function:
    def __init__(self, calc):
        self.__calc = calc

    def __call__(self, x):
        return self.__calc(x)


def simpson(func, a: float, b: float) -> float:
    return ((b - a) / 6) * (func(a) + 4 * func((a + b) / 2) + func(b))


# Dzielimy przedzial na podprzedzialy i dla kazdego liczymy wedlug wzoru Simpsona
# dopoki wynik nie osiągnie zadanej dokładności
def newton_cotes(func, a: float, b: float, epsilon: float) -> float:
    prev_result = 0
    while True:
        result = 0
        n = 1
        for i in range(n):
            lenght = (b - a) / n
            result += simpson(func, a + lenght * i, a + lenght * (i + 1))
        if result - prev_result < epsilon:
            break
        prev_result = result
    return result


# do porównania newtona_cotesa z naszą metodą musimy obliczyc granice
# nie wiem czy to jest dobrze, ta instrukcja jest zjebana
# przypomnij zeby pousuwac komentarze przed oddaniem xd
def newton_cotes_limit(func, epsilon: float) -> float:
    a = 0
    b = 0.5
    result = 0
    # granica do +1
    while True:
        integral = newton_cotes(func, a, b, epsilon)
        result += integral
        a = b
        b = b + (1 - b) / 2
        if abs(integral) < epsilon:
            break
    # granica do -1
    a = -0.5
    b = 0
    while True:
        integral = newton_cotes(func, a, b, epsilon)
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
    precision_choice = 0

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
    while float(precision_choice) <= 0:
        print("Podaj dokladnosc")
        precision_choice = input("\t>>>>")
    chosen_function = functions[int(function_choice) - 1][1]
    print(newton_cotes(chosen_function, float(a), float(b), float(precision_choice)))
    print(newton_cotes_limit(chosen_function, float(precision_choice)))


if __name__ == "__main__":
    main()
