from itertools import cycle

key = list('чугунныенебесачугунныенебеса')
file = open("variant12.txt", "r", encoding='utf-8')
text = file.read()
text = ''.join(text.split())
alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
            'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

key = list(map(lambda c: alphabet.index(c), key))

y = list(map(lambda c: alphabet.index(c), text))

y = [(x[0] - x[1]) % len(alphabet)
     for x in zip(y, cycle(key))]

open_text = ''.join(map(alphabet.__getitem__, y))
print(open_text)
output = open("open_text.txt", "w", encoding='utf-8')
output.write(open_text)
file.close()
