import tkinter as tk
from functions import *
import random
from time import sleep
from csv import writer, reader


root = tk.Tk()
root.title("2048")
root.configure(background="#bbada0")

W, H, score = 450, 450, 0
rand_list = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
animation = False
max_score = 0

text_score = tk.Label(root, text=f"Score: {score}",
                      bg="#bbada0", font="arial 20", pady=10)
text_score.grid(row=0, column=0)

text_max_score = tk.Label(root, text=f"Max Score: {max_score}",
                          bg="#bbada0", font="arial 20", pady=10)
text_max_score.grid(row=0, column=1)

canvas = tk.Canvas(width=W, height=H, background="#bbada0",
                   highlightthickness=1, highlightbackground="#bbada0")
canvas.grid(row=1, columnspan=2, padx=20, pady=10)


def restart():
    global data, score, max_score

    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    score = 0
    for i in range(2):
        zero_pos = []
        for pos in range(16):
            if data[pos] == 0:
                zero_pos.append(pos)
        data[random.choice(zero_pos)] = random.choice(rand_list)
    draw()
    max_score = max(max_score, score)
    text_max_score['text'] = f"Max score: {max_score}"
    text_score['text'] = f"Score: {score}"


btn = tk.Button(text="restart", command=restart)
btn.grid(row=2, columnspan=2, pady=10)


def create(column, row, number):
    global canvas
    canvas.create_rectangle(10+row*110, 10+column*110, 10+row*110+100, 10+column*110+100,
                            fill=bg_color(number), outline=bg_color(number))
    canvas.create_text(10+row*110+50, 10+column*110+50, text=number, fill=text_color(number), font="arial 30")


def draw():
    canvas.delete("all")
    for row in range(4):
        for col in range(4):
            if data[row*4+col] != 0:
                create(col, row, data[row*4+col])
            if data[row * 4 + col] == 0:
                canvas.create_rectangle(10+row*110, 10+col*110,
                                        10+row*110+100, 10+col*110+100,
                                        fill="#cdc1b4", outline="#cdc1b4")


def spawn(q, double_list):
    global data, animation
    animation = True
    x, y = 10 + q // 4 * 110 + 50, 10 + q % 4 * 110 + 50
    canvas.create_rectangle(x, y, x + 1, y + 1,
                            fill=bg_color(data[q]), outline=bg_color(data[q]))
    w = 1
    canvas.create_text(x, y, text=data[q], fill=text_color(data[q]), font=("arial", w))
    for i in range(1, 50, 4):
        canvas.create_rectangle(x - i, y - i, x + 1 + i, y + 1 + i,
                                fill=bg_color(data[q]), outline=bg_color(data[q]))
        canvas.create_text(x, y, text=data[q], fill=text_color(data[q]), font=("arial", int(i*29/50+1)))
        sleep(0.001)
        root.update()
    double_list.append(q)
    doubling(double_list)
    animation = False


def doubling(double_list):
    for j in range(1, 11):
        for coord in double_list:
            x_cords, y_cords = 10 + coord // 4 * 110, 10 + coord % 4 * 110
            if j < 6:
                canvas.create_rectangle(x_cords - j, y_cords - j, x_cords + 100 + j, y_cords + 100 + j,
                                        fill=bg_color(data[coord]), outline=bg_color(data[coord]))
            else:
                j = 10 - j
                draw()
                canvas.create_rectangle(x_cords - j, y_cords - j, x_cords + 100 + j, y_cords + 100 + j,
                                        fill=bg_color(data[coord]), outline=bg_color(data[coord]))
            canvas.create_text(x_cords+50, y_cords+50, text=data[coord],
                               fill=text_color(data[coord]), font=("arial", 30+j))
        sleep(0.001)
        root.update()


def add_block(double_list):
    draw()
    zero_pos = []
    for pos in range(16):
        if data[pos] == 0:
            zero_pos.append(pos)
    q = random.choice(zero_pos)
    data[q] = random.choice(rand_list)
    spawn(q, double_list)


def click(event):
    global score, animation, max_score
    check_move = False

    if not animation:
        double_list = []
        if event.keycode == 87 or event.keycode == 38:
            for col in range(4):
                for num in range(3):
                    if data[col*4+num] == 0 and data[col*4 + 1 + num] != 0:
                        data[col*4+num] = data[col*4 + 1 + num]
                        data[col * 4 + 1 + num] = 0
                        check_move = True
                for num in range(2):
                    if data[col*4+num] == 0 and data[col*4 + 1 + num] != 0:
                        data[col*4+num] = data[col*4 + 1 + num]
                        data[col * 4 + 1 + num] = 0
                        check_move = True
                if data[col*4] == 0 and data[col*4 + 1] != 0:
                    data[col*4] = data[col*4 + 1]
                    data[col * 4 + 1] = 0
                    check_move = True
                for num in range(3):
                    if data[col*4 + num] == data[col*4 + 1 + num] and data[col*4 + num] != 0:
                        double_list.append(col * 4 + num)
                        data[col * 4 + num] = data[col*4 + num] * 2
                        score += data[col*4 + num]
                        check_move = True
                        if num == 2:
                            data[col * 4 + 3] = 0
                        elif num == 1:
                            data[col * 4 + 2] = data[col * 4 + 3]
                            data[col * 4 + 3] = 0
                        elif num == 0:
                            data[col * 4 + 1] = data[col * 4 + 2]
                            data[col * 4 + 2] = data[col * 4 + 3]
                            data[col * 4 + 3] = 0

        if event.keycode == 65 or event.keycode == 37:
            for row in range(4):
                for num in range(3):
                    if data[num * 4 + row] == 0 and data[(num + 1) * 4 + row] != 0:
                        data[num * 4 + row] = data[(num + 1) * 4 + row]
                        data[(num + 1) * 4 + row] = 0
                        check_move = True
                for num in range(2):
                    if data[num * 4 + row] == 0 and data[(num + 1) * 4 + row] != 0:
                        data[num * 4 + row] = data[(num + 1) * 4 + row]
                        data[(num + 1) * 4 + row] = 0
                        check_move = True
                if data[row] == 0 and data[row + 4] != 0:
                    data[row] = data[row + 4]
                    data[4 + row] = 0
                    check_move = True
                for num in range(3):
                    if data[num * 4 + row] == data[(num + 1) * 4 + row] and data[num * 4 + row] != 0:
                        data[num * 4 + row] = data[num * 4 + row] * 2
                        score += data[num * 4 + row]
                        double_list.append(num * 4 + row)
                        check_move = True
                        if num == 2:
                            data[12 + row] = 0
                        elif num == 1:
                            data[8 + row] = data[12 + row]
                            data[12 + row] = 0
                        elif num == 0:
                            data[4 + row] = data[8 + row]
                            data[8 + row] = data[12 + row]
                            data[12 + row] = 0

        if event.keycode == 83 or event.keycode == 40:
            for col in range(4):
                for num in [3, 2, 1]:
                    if data[col * 4 + num] == 0 and data[col * 4 - 1 + num] != 0:
                        data[col * 4 + num] = data[col * 4 - 1 + num]
                        data[col * 4 - 1 + num] = 0
                        check_move = True
                for num in [3, 2]:
                    if data[col * 4 + num] == 0 and data[col * 4 - 1 + num] != 0:
                        data[col * 4 + num] = data[col * 4 - 1 + num]
                        data[col * 4 - 1 + num] = 0
                        check_move = True
                if data[col*4+3] == 0 and data[col*4 + 2] != 0:
                    data[col*4+3] = data[col*4 + 2]
                    data[col * 4 + 2] = 0
                    check_move = True
                for num in [3, 2, 1]:
                    if data[col * 4 + num] == data[col * 4 - 1 + num] and data[col * 4 + num] != 0:
                        data[col * 4 + num] = data[col * 4 + num] * 2
                        score += data[col * 4 + num]
                        double_list.append(col * 4 + num)
                        check_move = True
                        if num == 3:
                            data[col * 4 + 2] = data[col * 4 + 1]
                            data[col * 4 + 1] = data[col * 4]
                            data[col * 4] = 0
                        elif num == 2:
                            data[col * 4 + 1] = data[col * 4]
                            data[col * 4] = 0
                        elif num == 1:
                            data[col * 4] = 0

        if event.keycode == 68 or event.keycode == 39:
            for row in range(4):
                for num in [3, 2, 1]:
                    if data[num * 4 + row] == 0 and data[(num - 1) * 4 + row] != 0:
                        data[num * 4 + row] = data[(num - 1) * 4 + row]
                        data[(num - 1) * 4 + row] = 0
                        check_move = True
                for num in [3, 2]:
                    if data[num * 4 + row] == 0 and data[(num - 1) * 4 + row] != 0:
                        data[num * 4 + row] = data[(num - 1) * 4 + row]
                        data[(num - 1) * 4 + row] = 0
                        check_move = True
                if data[12 + row] == 0 and data[row + 8] != 0:
                    data[12 + row] = data[row + 8]
                    data[8 + row] = 0
                    check_move = True
                for num in [3, 2, 1]:
                    if data[num * 4 + row] == data[(num - 1) * 4 + row] and data[num * 4 + row] != 0:
                        data[num * 4 + row] = data[num * 4 + row] * 2
                        score += data[num * 4 + row]
                        double_list.append(num * 4 + row)
                        check_move = True
                        if num == 3:
                            data[8 + row] = data[4 + row]
                            data[4 + row] = data[row]
                            data[row] = 0
                        elif num == 2:
                            data[4 + row] = data[row]
                            data[row] = 0
                        elif num == 1:
                            data[row] = 0

        max_score = max(max_score, score)
        text_max_score['text'] = f"Max score: {max_score}"
        text_score['text'] = f"Score: {score}"
        if check_move:
            add_block(double_list)
        play()


def play():
    global score, max_score, data
    with open('log.txt', 'w') as file:
        write = writer(file)
        write.writerow([score])
        write.writerow([max_score])
        write.writerow(data)
        write.writerow([game_check(data)])
    if not game_check(data):
        canvas.create_rectangle(10, 10, W-10, H-10, stipple="gray25", fill="gray", outline="#bbada0")
        canvas.create_text(W/2, H/2, text="Game over", font="arial 50")


with open('log.txt', 'r') as file:
    read = reader(file)
    q = []
    for i in read:
        q.append(i)
max_score = int(q[2][0])
score = int(q[0][0])
data = []
for res in q[4]:
    data.append(int(res))

if q[6][0] == 'False':
    restart()
draw()
max_score = max(max_score, score)
text_max_score['text'] = f"Max score: {max_score}"
text_score['text'] = f"Score: {score}"
play()

root.bind('<Key>', click)
root.mainloop()
