import numpy as np
import matplotlib.pyplot as plt
file = open("variant12.txt", "r", encoding='utf-8')
text = file.read()
text = ''.join(text.split())
alphabet = np.array(['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                     'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'])

temporary = list(map(lambda c: np.where(alphabet == c)[0], text))

I_val = np.zeros(31)
for r in range(2, len(I_val)):
    I_of_Y = np.zeros(r)
    temp_rarity = np.zeros((r, len(alphabet)), dtype=int)
    for t in range(r):
        for k in range(t, len(temporary), r):
            tmp = temporary[k]
            temp_rarity[t][tmp] = temp_rarity[t][tmp] + 1

        I_of_Y[t] = np.dot(temp_rarity[t], temp_rarity[t] - 1) / (sum(temp_rarity[t]) * (sum(temp_rarity[t]) - 1))
    I_val[r] = sum(I_of_Y)/len(I_of_Y)
R = np.argmax(I_val)
lengths = np.arange(2, 31, 1, dtype=int)
I_of_r = I_val[2:]
print("Key length is ", R)
plt.figure(figsize=(9, 3))
plt.subplot(111)
plt.bar(lengths, I_of_r)
plt.suptitle('Індекс відповідності для ключів довжиною 2-30')
plt.show()
most_common_letter = 14
key = np.zeros(R, dtype=int)
for a in range(R):
    block_rarity = np.zeros(len(alphabet), dtype=int)
    most_common_in_block = 0
    for b in range(a, len(temporary), R):
        block_rarity[temporary[b]] += 1
    most_common_in_block = np.argmax(block_rarity)
    key[a] = most_common_in_block - most_common_letter
print("key is: ", alphabet[key])
file.close()
