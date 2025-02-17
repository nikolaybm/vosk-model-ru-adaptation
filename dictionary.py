#!/usr/bin/python3
# -- coding: utf-8 --

import sys

softletters = set("яёюиье")
startsyl = set("#ъьаяоёуюэеиы-")
others = set(["#", "+", "-", "ь", "ъ"])

softhard_cons = {
    "б": "b", "в": "v", "г": "g", "Г": "g", "д": "d",
    "з": "z", "к": "k", "л": "l", "м": "m", "н": "n",
    "п": "p", "р": "r", "с": "s", "т": "t", "ф": "f", "х": "h"
}

other_cons = {
    "ж": "zh", "ц": "c", "ч": "ch", "ш": "sh", "щ": "sch", "й": "j"
}

vowels = {
    "а": "a", "я": "a", "у": "u", "ю": "u", "о": "o",
    "ё": "o", "э": "e", "е": "e", "и": "i", "ы": "y"
}

def pallatize(phones):
    for i in range(len(phones) - 1):
        phone, stress = phones[i]
        next_phone, _ = phones[i + 1]
        if phone in softhard_cons:
            phones[i] = (softhard_cons[phone] + ("j" if next_phone in softletters else ""), stress)
        elif phone in other_cons:
            phones[i] = (other_cons[phone], stress)

def convert_vowels(phones):
    new_phones = []
    prev = ""
    for phone, stress in phones:
        if prev in startsyl and phone in "яюеё":
            new_phones.append("j")
        new_phones.append(vowels.get(phone, phone) + (str(stress) if phone in vowels else ""))
        prev = phone
    return new_phones

def convert(stressword):
    phones = list("#" + stressword + "#")

    stress_phones = []
    stress = 0
    for phone in phones:
        if phone == "+":
            stress = 1
        else:
            stress_phones.append((phone, stress))
            stress = 0
    
    pallatize(stress_phones)
    phones = convert_vowels(stress_phones)
    phones = [x for x in phones if x not in others]
    
    return " ".join(phones)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <input_file>")
        sys.exit(1)
    
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        for line in f:
            stressword = line.strip()
            print(stressword.replace("+", ""), convert(stressword), sep="\t")
