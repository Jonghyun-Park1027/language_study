BACKGROUND_COLOR = "#B1DDC6"

import random
from tkinter import *

import pandas as pd

try:
    data = pd.read_csv("data/words_to_learn(day object).csv")
except FileNotFoundError:

    read_data = pd.read_csv("data/english_words.csv")
    read_data.to_csv("data/words_to_learn(day object).csv", index = False)
    data = pd.read_csv("data/words_to_learn(day object).csv")
df = pd.DataFrame.to_dict(data)
to_learn = data.to_dict(orient="records")
# test = pd.DataFrame(to_learn)
# print(test)
current_card = {}
num = 0

def right_text():
    global current_card, num
    global flip_timer
    window.after_cancel(flip_timer)
    try:
        to_learn.remove(current_card)
        next_to_learn = pd.DataFrame(to_learn)
    except ValueError:
        pass
    else:
        next_to_learn.to_csv("data/words_to_learn(day object).csv", index=False)
        # load_data()
    # print(to_learn)
    current_card = to_learn[num]
    canvas.itemconfigure(canvas_image, image = card_front_img)
    canvas.itemconfigure(card_title, text = "English", fill = "black")
    canvas.itemconfigure(card_word, text = current_card["English"], fill= "black")
    flip_timer = window.after(3000, next_english)


def first_text():
    global current_card, num
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = to_learn[0]
    canvas.itemconfigure(canvas_image, image = card_front_img)
    canvas.itemconfigure(card_title, text = "English", fill = "black")
    canvas.itemconfigure(card_word, text = current_card["English"], fill= "black")
    flip_timer = window.after(3000, next_english)
def wrong_text():
    global current_card, num
    global flip_timer
    num += 1
    window.after_cancel(flip_timer)
    current_card = to_learn[num]
    canvas.itemconfigure(canvas_image, image = card_front_img)
    canvas.itemconfigure(card_title, text = "English", fill = "black")
    canvas.itemconfigure(card_word, text = current_card["English"], fill= "black")
    flip_timer = window.after(3000, next_english)


def next_english():
    global num
    canvas.itemconfigure(canvas_image, image = card_back_img)
    canvas.itemconfigure(card_title, text = "Korean", fill = "white")
    try :
        canvas.itemconfigure(card_word, text = current_card["Korean"], fill= "white")
    except KeyError:
        print(num)
        wrong_text()


window = Tk()
window.title("Flashy")
# window.geometry("400x400")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=first_text)
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
right_img = PhotoImage(file="./images/right.png")
wrong_img = PhotoImage(file="./images/wrong.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=["Ariel", 40, "italic"] )
card_word = canvas.create_text(400, 285, text="Word", font=["Ariel", 60, "bold"] )

canvas.grid(row=0, column=0, columnspan=2)
wrong_button = Button(image=wrong_img, highlightthickness=0, command=wrong_text)
wrong_button.grid(row=1, column=0)
right_button = Button(image=right_img, highlightthickness=0, command=right_text)
right_button.grid(row=1, column=1)


window.mainloop()