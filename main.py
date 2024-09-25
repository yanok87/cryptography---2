f = open("text.txt", "r")
text_to_incrypt = f.read()


def generate_key(text, key):
    key = list(key)
    if len(text) == len(key):
        return "".join(key)
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


def vigenere_encrypt(text, key):
    encrypted_text = []
    for i in range(len(text)):
        if text[i].isalpha():
            shift = (ord(text[i].upper()) + ord(key[i])) % 26
            encrypted_char = chr(shift + 65)
            encrypted_text.append(encrypted_char)
        else:
            encrypted_text.append(text[i])
    return "".join(encrypted_text)


def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            shift = (ord(ciphertext[i]) - ord(key[i]) + 26) % 26
            decrypted_char = chr(shift + 65)
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(ciphertext[i])
    return "".join(decrypted_text)


# Приклад використання
key = "CRYPTOGRAPHY"
key_generated = generate_key(text_to_incrypt, key)

encrypted_text = vigenere_encrypt(text_to_incrypt, key_generated)
decrypted_text = vigenere_decrypt(encrypted_text, key_generated)

# print("Зашифрований текст:", encrypted_text)
# print("Розшифрований текст:", decrypted_text)


# Тест Фрідмана для оцінки довжини ключа
def friedman_test(ciphertext):
    n = len(ciphertext)
    freq = [ciphertext.count(chr(i + 65)) for i in range(26)]
    IC = sum([f * (f - 1) for f in freq]) / (n * (n - 1))
    key_length_estimate = 0.027 / (IC - 0.0385) if IC != 0 else 1
    return round(key_length_estimate)


# print(friedman_test(text_to_incrypt))
# Застосування тесту Касіскі потребує реалізації пошуку повторів і аналізу їх відстаней
# Алгоритм не включений, оскільки це складна операція для ручної реалізації


def simple_transposition_encrypt(text, key):
    key_length = len(key)
    table = ["" for _ in range(key_length)]

    for i, char in enumerate(text):
        table[i % key_length] += char

    return "".join(table)


def simple_transposition_decrypt(ciphertext, key):
    key_length = len(key)
    n = len(ciphertext)
    num_rows = n // key_length
    remainder = n % key_length

    table = ["" for _ in range(key_length)]
    pos = 0

    for i in range(key_length):
        if i < remainder:
            table[i] = ciphertext[pos : pos + num_rows + 1]
            pos += num_rows + 1
        else:
            table[i] = ciphertext[pos : pos + num_rows]
            pos += num_rows

    decrypted_text = []
    for i in range(num_rows + (1 if remainder > 0 else 0)):
        for j in range(key_length):
            if i < len(table[j]):
                decrypted_text.append(table[j][i])

    return "".join(decrypted_text)


# Приклад використання
key = "SECRET"
ciphertext = simple_transposition_encrypt(text_to_incrypt, key)
decrypted_text = simple_transposition_decrypt(ciphertext, key)

# print("Зашифрований текст:", ciphertext)
# print("Розшифрований текст:", decrypted_text)


def double_transposition_encrypt(text, key1, key2):
    return simple_transposition_encrypt(simple_transposition_encrypt(text, key1), key2)


def double_transposition_decrypt(ciphertext, key1, key2):
    return simple_transposition_decrypt(
        simple_transposition_decrypt(ciphertext, key2), key1
    )


# Приклад використання
key1 = "SECRET"
key2 = "CRYPTO"
ciphertext = double_transposition_encrypt(text_to_incrypt, key1, key2)
decrypted_text = double_transposition_decrypt(ciphertext, key1, key2)

# print("Зашифрований текст:", ciphertext)
# print("Розшифрований текст:", decrypted_text)

import math


# Функція для додавання заповнювачів, щоб довжина тексту ділилася на кількість стовпців
def pad_text(text, num_cols):
    padding_size = num_cols - (len(text) % num_cols)
    if padding_size != num_cols:
        text += " " * padding_size  # Додаємо пробіли як заповнювач
    return text


# Функція для шифрування (записуємо текст в таблицю по рядках і зчитуємо по стовпцях)
def table_encrypt(text, key):
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)

    # Додаємо заповнювачі до тексту
    text = pad_text(text, num_cols)

    # Створюємо таблицю
    table = [["" for _ in range(num_cols)] for _ in range(num_rows)]
    index = 0

    # Заповнюємо таблицю текстом по рядках
    for i in range(num_rows):
        for j in range(num_cols):
            if index < len(text):
                table[i][j] = text[index]
                index += 1

    # Сортуємо ключ для правильного порядку стовпців
    sorted_key = sorted(list(key))

    # Читаємо текст по стовпцях відповідно до відсортованого ключа
    ciphertext = ""
    for k in sorted_key:
        col_index = key.index(k)
        for i in range(num_rows):
            if table[i][col_index] != "":
                ciphertext += table[i][col_index]

    return ciphertext


# Функція для дешифрування (записуємо текст в таблицю по стовпцях і зчитуємо по рядках)
def table_decrypt(ciphertext, key):
    num_cols = len(key)
    num_rows = math.ceil(len(ciphertext) / num_cols)

    # Створюємо порожню таблицю для дешифрування
    table = [["" for _ in range(num_cols)] for _ in range(num_rows)]

    # Сортуємо ключ
    sorted_key = sorted(list(key))

    # Заповнюємо таблицю за стовпцями відповідно до відсортованого ключа
    index = 0
    for k in sorted_key:
        col_index = key.index(k)
        for i in range(num_rows):
            if index < len(ciphertext):
                table[i][col_index] = ciphertext[index]
                index += 1

    # Зчитуємо таблицю по рядках для отримання початкового тексту
    decrypted_text = ""
    for i in range(num_rows):
        for j in range(num_cols):
            if table[i][j] != "":
                decrypted_text += table[i][j]

    return decrypted_text.strip()  # Видаляємо зайві пробіли після дешифрування


# Приклад використання
key = "MATRIX"

# Шифрування
# ciphertext = table_encrypt(text_to_incrypt, key)
# print("Зашифрований текст:", ciphertext)

# Дешифрування
# decrypted_text = table_decrypt(ciphertext, key)
# print("Розшифрований текст:", decrypted_text)


# Шифрування тексту спочатку Віженером, потім Табличним шифром
vigenere_key = "CRYPTO"
table_key = "MATRIX"

vigenere_encrypted = vigenere_encrypt(
    text_to_incrypt, generate_key(text_to_incrypt, vigenere_key)
)
table_encrypted = table_encrypt(vigenere_encrypted, table_key)
print("Текст, зашифрований Віженером, потім Табличним шифром:", table_encrypted)

# Дешифрування тексту у зворотному порядку
table_decrypted = table_decrypt(table_encrypted, table_key)
vigenere_decrypted = vigenere_decrypt(
    table_decrypted, generate_key(table_decrypted, vigenere_key)
)
print("Розшифрований текст:", vigenere_decrypted)

f.close()
