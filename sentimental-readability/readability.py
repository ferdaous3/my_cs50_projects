import re

def count_letters(text):
    return sum(1 for char in text if char.isalpha())

def count_words(text):
    return len(text.split())

def count_sentences(text):
    return len(re.findall(r'[.!?]', text))

def compute_readability(text):
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    L = letters / words * 100
    S = sentences / words * 100

    index = 0.0588 * L - 0.296 * S - 15.8

    if index < 1:
        grade = "Before Grade 1"
    elif index >= 16:
        grade = "Grade 16+"
    else:
        grade = f"Grade {round(index)}"

    return grade

# استخدام البرنامج
text = input("Text: ")
result = compute_readability(text)
print(result)
