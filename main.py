BACKGROUND_COLOR = "#B1DDC6"

import random
from tkinter import *
import pandas as pd
from googletrans import Translator

# 번역기 초기화
translator = Translator()

# 번역 캐시 (같은 단어 재번역 방지)
translation_cache = {}

def translate_word(word):
    """영어 단어를 한국어로 번역"""
    if word in translation_cache:
        return translation_cache[word]

    try:
        translation = translator.translate(word, src='en', dest='ko')
        korean = translation.text
        translation_cache[word] = korean
        return korean
    except Exception as e:
        print(f"번역 오류: {e}")
        return "[번역 실패]"

try:
    data = pd.read_csv("data/words_to_learn(day object).csv", header=None, names=['word'])
except FileNotFoundError:
    read_data = pd.read_csv("data/english_words.csv")
    read_data.to_csv("data/words_to_learn(day object).csv", index=False)
    data = pd.read_csv("data/words_to_learn(day object).csv", header=None, names=['word'])

to_learn = data['word'].tolist()
current_card = {}
num = 0

def adjust_text_size(text, is_korean=False):
    """텍스트 길이에 따라 폰트 크기와 줄바꿈 조정"""
    text_length = len(text)

    if is_korean:
        # 한국어는 더 짧은 기준으로 폰트 크기 조정
        if text_length > 20:
            font_size = 35
        elif text_length > 12:
            font_size = 45
        else:
            font_size = 60

        # 한국어 줄바꿈 처리 (쉼표, 공백 기준)
        if text_length > 12:
            # 쉼표로 분리
            parts = text.split(',')
            if len(parts) > 1:
                formatted_text = ',\n'.join(parts)
            else:
                # 공백으로 분리
                words = text.split()
                if len(words) > 1:
                    lines = []
                    current_line = []
                    for word in words:
                        current_line.append(word)
                        if len(' '.join(current_line)) > 15:
                            if len(current_line) > 1:
                                current_line.pop()
                                lines.append(' '.join(current_line))
                                current_line = [word]
                            else:
                                lines.append(word)
                                current_line = []
                    if current_line:
                        lines.append(' '.join(current_line))
                    formatted_text = '\n'.join(lines)
                else:
                    formatted_text = text
        else:
            formatted_text = text
    else:
        # 영어 텍스트 길이에 따라 폰트 크기 조정
        if text_length > 30:
            font_size = 35
        elif text_length > 20:
            font_size = 45
        else:
            font_size = 60

        # 단어가 너무 길면 줄바꿈 처리
        if text_length > 20:
            words = text.split()
            lines = []
            current_line = []

            for word in words:
                current_line.append(word)
                # 현재 라인의 길이가 너무 길면 줄바꿈
                if len(' '.join(current_line)) > 25:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []

            if current_line:
                lines.append(' '.join(current_line))

            formatted_text = '\n'.join(lines)
        else:
            formatted_text = text

    return formatted_text, font_size

def right_text():
    global current_card, num, flip_timer
    window.after_cancel(flip_timer)

    try:
        to_learn.remove(current_card["English"])
        next_to_learn = pd.DataFrame(to_learn, columns=['word'])
        next_to_learn.to_csv("data/words_to_learn(day object).csv", index=False, header=False)
    except ValueError:
        pass

    if num < len(to_learn):
        english_word = to_learn[num]
        current_card = {"English": english_word, "Korean": translate_word(english_word)}
        canvas.itemconfigure(canvas_image, image=card_front_img)
        canvas.itemconfigure(card_title, text="English", fill="black")
        formatted_text, font_size = adjust_text_size(current_card["English"])
        canvas.itemconfigure(card_word, text=formatted_text, fill="black", font=["Ariel", font_size, "bold"])
        flip_timer = window.after(3000, next_english)


def first_text():
    global current_card, num, flip_timer
    if len(to_learn) > 0:
        english_word = to_learn[0]
        current_card = {"English": english_word, "Korean": translate_word(english_word)}
        canvas.itemconfigure(canvas_image, image=card_front_img)
        canvas.itemconfigure(card_title, text="English", fill="black")
        formatted_text, font_size = adjust_text_size(current_card["English"])
        canvas.itemconfigure(card_word, text=formatted_text, fill="black", font=["Ariel", font_size, "bold"])
        flip_timer = window.after(3000, next_english)

def wrong_text():
    global current_card, num, flip_timer
    num += 1
    window.after_cancel(flip_timer)
    if num < len(to_learn):
        english_word = to_learn[num]
        current_card = {"English": english_word, "Korean": translate_word(english_word)}
        canvas.itemconfigure(canvas_image, image=card_front_img)
        canvas.itemconfigure(card_title, text="English", fill="black")
        formatted_text, font_size = adjust_text_size(current_card["English"])
        canvas.itemconfigure(card_word, text=formatted_text, fill="black", font=["Ariel", font_size, "bold"])
        flip_timer = window.after(3000, next_english)

def next_english():
    global num
    canvas.itemconfigure(canvas_image, image=card_back_img)
    canvas.itemconfigure(card_title, text="Korean", fill="white")
    try:
        formatted_text, font_size = adjust_text_size(current_card["Korean"], is_korean=True)
        canvas.itemconfigure(card_word, text=formatted_text, fill="white", font=["Ariel", font_size, "bold"])
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