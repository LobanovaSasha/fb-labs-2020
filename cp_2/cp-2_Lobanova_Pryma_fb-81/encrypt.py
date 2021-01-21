from itertools import cycle

key = "александралобанова"

alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
            'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
file = open('sasha.txt', "r", encoding="utf-8")

small_text = file.read()

temporary = list(map(lambda c: alphabet.index(c), small_text))

encoded_key = list(map(lambda c: alphabet.index(c), key))

temporary = [(x[0] + x[1]) % len(alphabet)
             for x in zip(temporary, cycle(encoded_key))]

cipher_text = ''.join(map(alphabet.__getitem__, temporary))
output = open("cipher_text_ r={}.txt".format(len(key)), "w", encoding='utf-8')
output.write(cipher_text)
output.write("\n\n key is ")
output.write(key)
file.close()
