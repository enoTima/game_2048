def bg_color(number):
    if number == 2:
        return "#eee4da"
    if number == 2**2:
        return "#ede0c8"
    if number == 2**3:
        return "#f2b179"
    if number == 2**4:
        return "#f59563"
    if number == 2**5:
        return "#ff775c"
    if number == 2**6:
        return "#e64c2e"
    if number == 2**7:
        return "#ede291"
    if number == 2**8:
        return "#fce130"
    if number == 2**9:
        return "#ffdb4a"
    if number == 2**10:
        return "#edc53f"
    if number == 2**11:
        return "#edc22e"


def text_color(number):
    if number == 2:
        return "#776e65"
    if number == 2 ** 2:
        return "#776e65"
    if number == 2 ** 3:
        return "#f9f6f2"
    if number == 2 ** 4:
        return "#f9f6f2"
    if number == 2 ** 5:
        return "#f9f6f2"
    if number == 2 ** 6:
        return "#f9f6f2"
    if number == 2 ** 7:
        return "#f9f6f2"
    if number == 2 ** 8:
        return "#f9f6f2"
    if number == 2 ** 9:
        return "#f9f6f2"
    if number == 2 ** 10:
        return "#f9f6f2"
    if number == 2 ** 11:
        return "#f9f6f2"


def game_check(data):
    if 0 in data:
        return True
    for i in range(4):
        for j in range(4):
            if j != 3:
                if data[i * 4 + j] == data[i * 4 + j + 1]:
                    return True
            if i != 3:
                if data[i * 4 + j] == data[(i + 1) * 4 + j]:
                    return True
    return False
