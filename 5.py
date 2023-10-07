# Лабораторная работа #5 (5)
# @ Кудлай Никита, PЗ2141
# Многочлены Лагрнажа и Гаусса
import numpy as np
import matplotlib.pyplot as plt
from math import sin, sqrt, factorial

flag = True
def lagrange_polynomial(dots, x): # Многочлен Лагранжа
    result = 0

    n = len(dots)
    for i in range(n):
        c1 = c2 = 1
        for j in range(n):
            if i != j:
                c1 *= x - dots[j][0]
                c2 *= dots[i][0] - dots[j][0]
        result += dots[i][1] * c1 / c2

    return result


def p_cal(p, n, forward=True):
    temp = p
    for i in range(0, n-1):
        if forward:
            if (i % 2 == 0):
                temp *= (p - i//2 - 1)
            else:
                temp *= (p + i//2 + 1)
        else:
            if (i % 2 == 1):
                temp *= (p - i//2 - 1)
            else:
                temp *= (p + i//2 + 1)
    return temp


def u_cal(u, n):
    if (n == 0):
        return 1;

    temp = u;
    for i in range(1, int(n / 2 + 1)):
        temp = temp * (u - i);

    for i in range(1, int(n / 2)):
        temp = temp * (u + i);

    return temp;
def gauss_polynomial(dots, x, flag): # Многочлен Гаусса
    n = len(dots)
    h = dots[1][0] - dots[0][0]
    a = [[0] * n for _ in range(n)]
    t = (x - dots[n//2][0])/h
    for i in range(n):
        a[i][0] = dots[i][1]
    for i in range(1, n):
        for j in range(n - i):
            a[j][i] = a[j + 1][i - 1] - a[j][i - 1]
    if not flag:
        print("Разности:")
        for i in range(len(a)):
            for j in range(n - i):
                print(a[i][j], end = " ")
            print()
    if n % 2 == 1:
        middle = n // 2
        result = a[middle][0]

        if not flag:
            print("Средняя точка: ", result)
        if x > dots[middle][0] or not flag: # Первая интерполяционная формула Гаусса
            if not flag:
                print("Члены для первой формулы Гаусса:")
            for i in range(1, n):
                result += (p_cal(t, i) * a[(n-i)//2][i]) / factorial(i)
                if not flag:
                    print(a[(n-i)//2][i])

        if x <= dots[middle][0] or not flag: # Вторая интерполяционная формула Гаусса
            #result = a[(n-1) // 2+1][0]
            if not flag:
                print("Члены для второй формулы Гаусса:")
            for i in range(1, n):
                if n-i % 2 == 0:
                    result += (p_cal(t, i, False) * a[(n-i)//2][i]) / factorial(i)
                    if not flag:
                        print(a[(n-i)//2][i])
                else:
                    result += (p_cal(t, i, False) * a[(n-i+1)//2-1][i]) / factorial(i)
                    if not flag:
                        print(a[(n-i+1)//2-1][i])

        return result
    else:
        result = (a[n // 2][0] + a[n // 2-1][0]) / 2
        k = int(n / 2 - 1);
        u = (x - dots[k][0]) / (dots[1][0] - dots[0][0])
        if not flag:
            print("Члены для формулы Бесселя:")
        for i in range(1, n):
            if (i % 2):
                result = result + ((u - 0.5) * u_cal(u, i - 1) * a[k][i]) / factorial(i)
                if not flag:
                    print(a[k][i])
            else:
                result = result + (u_cal(u, i) * (a[k][i] + a[k - 1][i]) / (factorial(i) * 2))
                k -= 1
                if not flag:
                    print(a[k][i])
        return result

def plot(x, y, plot_x, plot_y): # Отрисовать график по заданным координатам узлов и точкам многочлена
    ax = plt.gca()
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.plot(1, 0, marker=">", ms=5, color='k',
            transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k',
            transform=ax.get_xaxis_transform(), clip_on=False)

    # Отрисовываем график
    plt.plot(x, y, 'o', plot_x, plot_y)
    plt.show(block=False)


def getfunc(func_id): # Получить выбранную функцию
    if func_id == '1':
        return lambda x: sqrt(x)
    elif func_id == '2':
        return lambda x: x ** 2
    elif func_id == '3':
        return lambda x: sin(x)
    else:
        return None


def make_dots(f, a, b, n):
    dots = []

    h = (b - a) / (n - 1)
    for i in range(n):
        dots.append((a, f(a)))
        a += h

    return dots


def getdata_input(): # Получить данные с клавиатуры
    data = {}

    print("\nВыберите метод интерполяции.")
    print(" 1 — Многочлен Лагранжа")
    print(" 2 — Многочлен Гаусса")
    while True:
        try:
            method_id = input("Метод решения: ")
            if method_id != '1' and method_id != '2':
                raise AttributeError
            break
        except AttributeError:
            print("Метода нет в списке.")
    data['method_id'] = method_id

    print("\nВыберите способ ввода исходных данных.")
    print(" 1 — Набор точек")
    print(" 2 — Функция")
    while True:
        try:
            input_method_id = input("Способ: ")
            if input_method_id != '1' and input_method_id != '2':
                raise AttributeError
            break
        except AttributeError:
            print("Способа нет в списке.")

    dots = []
    if input_method_id == '1':
        print("Вводите координаты через пробел, каждая точка с новой строки.")
        print("Чтобы закончить, введите 'end'.")
        while True:
            try:
                current = input().upper()
                if current == 'END':
                    if len(dots) < 2:
                        raise AttributeError
                    break
                x, y = map(float, current.split())
                dots.append((x, y))
            except ValueError:
                print("Введите точку повторно - координаты должны быть числами!")
            except AttributeError:
                print("Минимальное количество точек - две!")
    elif input_method_id == '2':
        print("\nВыберите функцию.")
        print(" 1 — √x")
        print(" 2 - x²")
        print(" 3 — sin(x)")
        while True:
            try:
                func_id = input("Функция: ")
                func = getfunc(func_id)
                if func is None:
                    raise AttributeError
                break
            except AttributeError:
                print("Функции нет в списке.")
        print("\nВведите границы отрезка.")
        while True:
            try:
                a, b = map(float, input("Границы отрезка: ").split())
                if a > b:
                    a, b = b, a
                break
            except ValueError:
                print("Границы отрезка должны быть числами, введенными через пробел.")
        print("\nВыберите количество узлов интерполяции.")
        while True:
            try:
                n = int(input("Количество узлов: "))
                if n < 2:
                    raise ValueError
                break
            except ValueError:
                print("Количество узлов должно быть целым числом > 1.")
        dots = make_dots(func, a, b, n)
    data['dots'] = dots

    print("\nВведите значение аргумента для интерполирования.")
    while True:
        try:
            x = float(input("Значение аргумента: "))
            break
        except ValueError:
            print("Значение аргумента должно быть числом.")
    data['x'] = x

    return data


def main():
    print("\tЛабораторная работа #5 (5)")
    print("\tИнтерполяция функций")

    data = getdata_input()
    x = np.array([dot[0] for dot in data['dots']])
    y = np.array([dot[1] for dot in data['dots']])
    plot_x = np.linspace(np.min(x), np.max(x), 100)
    plot_y = None
    answer_l = lagrange_polynomial(data['dots'], data['x'])
    answer_g = (gauss_polynomial(data['dots'], data['x'], True))
    if data['method_id'] == '1':
        answer = answer_l
        plot_y = [lagrange_polynomial(data['dots'], x) for x in plot_x]
    elif data['method_id'] == '2':
        answer = answer_g
        plot_y = [(gauss_polynomial(data['dots'], x, True)) for x in plot_x]
        gauss_polynomial(data['dots'], plot_x[0], False)
    else:
        answer = None

    if answer is not None:
        plot(x, y, plot_x, plot_y)

    print("\n\nРезультаты вычисления.")
    print(f"Приближенное значение функции по Гауссу: {answer_g}")
    print(f"Приближенное значение функции по Лагранжу: {answer_l}")

    input("\n\nНажмите Enter, чтобы выйти.")


main()
