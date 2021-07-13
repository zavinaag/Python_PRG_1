characters = {}
result = {}

def ccount(word):
    for letter in str.lower(word):
        if letter not in characters:
            if letter == ' ' or letter == '':
                if '-_-' in characters:
                    characters['-_-'] += 1
                else:
                    characters.setdefault('-_-',1)
            elif letter == '_':
                if '__' in characters:
                    characters['__'] += 1
                else:
                    characters.setdefault('__',1)
            else:
                characters.setdefault(letter, 1)
        else:
            characters[letter] += 1
    result = characters.copy()
    characters.clear()
    return result
