pattern = ['запретил', 'букву']
template = [input()]
alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч',
 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'][:: -1]

template.extend(pattern)

print(template)

for idx in range(len(template)):
    letter = alphabet.pop()
    if letter in template:
        print(template.lstrip(), letter)
        template = template.replace(letter, '')
    if len(template) == template.count(' '):
        break

