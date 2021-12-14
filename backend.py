from math import sqrt, fabs


def getFileData(filename):
    result = []

    with open(filename, 'r') as openReadFile:
        for line in openReadFile:
            result = line.split()

            for i, j in enumerate(result):
                result[i] = float(result[i].replace(',', '.'))

            print(result)

            return result


def avg_data(mas):
    s = 0
    for i in range(0, len(mas)):
        s += mas[i];
    avg = s / len(mas)

    print(avg)

    return avg


def deviation_offset(mas, avg):
    n = len(mas)

    temp = 0
    for i in mas:
        temp += (i - avg) ** 2

    return sqrt(temp / n)


def quantile(mas, deviation, avg):
    n = len(mas)

    temp = 0
    for i in mas:
        temp += fabs(i - avg)

    return temp / n / deviation


if __name__ == '__main__':
    # FILENAME = input()
    FILENAME = 'G_v22_a.txt'

    fileData = getFileData(FILENAME)

    # Среднее значение по выборке
    avg_curr = avg_data(fileData)

    # Смещенное среднее квадратическое отклонение
    deviation_curr = deviation_offset(fileData, avg_curr)

    # Отношение квантиля d~
    quantile_curr = quantile(fileData, deviation_curr, avg_curr)
