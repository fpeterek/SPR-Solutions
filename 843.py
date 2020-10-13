
class Word:

    @staticmethod
    def extract_pattern(word):
        return ''.join([str(word.index(char)) for char in word])

    def __init__(self, word):
        self.word = word
        self.pattern = Word.extract_pattern(word)


class Decryptor:
    def __init__(self, dct):
        self.dct = dct
        self.dct_words = {w.word for w in dct}
        # self.dct_patterns = {w.pattern: list(filter(lambda x: x.pattern == w.pattern, dct)) for w in dct}
        self.viable_by_pattern = None
        self.word_patterns = None
        self.distinct = None
        self.viable = None
        self.sentence = None
        self.letters_to_find = 100

    @staticmethod
    def replace_letters(word, letters):
        return ''.join([letters.get(char, '*') for char in word])

    def is_valid_word(self, word):
        return word in self.dct_words

    def test(self, known_letters):
        return all(map(lambda word: self.is_valid_word(Decryptor.replace_letters(word, known_letters)), self.distinct))

    def get_matches(self, decryptee, known_letters):
        pattern = self.word_patterns.get(decryptee, '')
        matches = []
        possible_matches = self.viable_by_pattern.get(pattern, [])

        for wi, w in enumerate(possible_matches):
            for i, l in enumerate(decryptee):
                if l in known_letters and w.word[i] != known_letters[l]:
                    break 
                matches.append(w)

        return matches

    def decrypt_with_context(self, current_index, known_letters):
        if current_index >= len(self.distinct) and len(known_letters) < self.letters_to_find:
            return {}

        if len(known_letters) >= self.letters_to_find:
            if self.test(known_letters):
                return known_letters
            return {}
            # return known_letters

        decryptee = self.distinct[current_index]
        
        if all(map(lambda char: char in known_letters, decryptee)):
            if not self.is_valid_word(Decryptor.replace_letters(decryptee, known_letters)):
                return {}
            return self.decrypt_with_context(current_index+1, known_letters)

        possible_matches = self.get_matches(decryptee, known_letters)

        for match in possible_matches:
            is_valid = True
            known_copy = dict(known_letters)
            known_letter_set = set(known_copy.values())
            for i, l in enumerate(decryptee):
                if l in known_copy and match.word[i] != known_copy[l]:
                    is_valid = False
                    break
                if l not in known_copy:
                    if match.word[i] in known_letter_set:
                        is_valid = False
                        break
                    known_copy[l] = match.word[i]
                    known_letter_set.add(match.word[i])
            if not is_valid:
                continue
            letters = self.decrypt_with_context(current_index+1, known_copy)
            if letters:
                return letters

        return {}

    def get_result(self, letter_dict):
        return ''.join(' ' if char.isspace() else letter_dict.get(char, '*') for char in self.sentence)

    def decrypt_sentence(self, sentence):
        self.sentence = sentence
        self.distinct = set(sentence.split())

        self.word_patterns = {word: Word.extract_pattern(word) for word in self.distinct}

        self.viable = list(filter(lambda dword: dword.pattern in self.word_patterns.values(), self.dct))
        self.viable_by_pattern = {w.pattern: list(filter(lambda x: x.pattern == w.pattern, self.viable)) for w in self.viable}

        self.letters_to_find = len(set(sentence) - set(' '))

        self.distinct = sorted(self.distinct, key=lambda word: len(self.viable_by_pattern.get(Word.extract_pattern(word), [])))

        return self.get_result(self.decrypt_with_context(0, {}))


def load_words():
    words = int(input())
    dct = []
    for _ in range(words):
        dct.append(Word(input()))
    return dct


def decrypt_words():
    decryptor = Decryptor(load_words())
    while True:
        sentence = input()
        if not sentence or sentence.isspace():
            break
        print(decryptor.decrypt_sentence(sentence))


if __name__ == '__main__':
    try:
        decrypt_words()
    except EOFError:
        # Input on Online Judge doesn't end with an empty line, which causes input() to raise EOFError
        pass
