import requests
from collections import defaultdict


class Wordle:
    def __init__(self, dictionary='http://www.mieliestronk.com/corncob_caps.txt'):
        self.valid = {'M', 'E', 'I', 'J', 'H', 'X', 'O', 'Z', 'Q', 'W', 'K', 'F', 'Y',
                      'B', 'L', 'T', 'R', 'A', 'V', 'G', 'U', 'C', 'P', 'S', 'D', 'N'}
        self.words = self._load_words(dictionary)

    def __call__(self, *args, **kwargs):
        start = self.start_word(self.words)
        print([w for w in start])
        while True:
            self.words = self.remove_letter()
            print(self.start_word(self.words))

    @staticmethod
    def _load_words(dictionary):
        words = list()
        for word in requests.get(dictionary).text.splitlines():
            if len(word) == 5:
                words.append(word)
        return words

    def letter_count(self, len=10):
        alpha = dict()
        for word in self.words:
            for l in word:
                alpha[l] = alpha.get(l, 0) + 1
        return sorted(zip(alpha.values(), alpha.keys()), reverse=True)[:len]

    def start_word(self, words):
        letters = self.letter_count(6)
        tmp_words = list()
        for word in self.words:
            if all(x in [l[1] for l in letters] for x in word):
                tmp_words.append(word)
        unique = dict()
        for word in tmp_words:
            alpha = dict()
            for l in word:
                alpha[l] = alpha.get(l, 0) + 1
            unique[word] = len(alpha)
        a = defaultdict(list)
        for u, n in unique.items():
            a[n].append(u)
        if a[5]:
            return a[5]
        elif a[4]:
            return a[4]
        else:
            return a[3]

    def remove_letter(self):
        letters = input("Enter wrong letters: ")
        for l in letters.upper():
            self.valid.discard(l)
        still_valid = list()
        for word in self.words:
            if all(x in self.valid for x in word):
                still_valid.append(word)
        return still_valid


if __name__ == '__main__':
    w = Wordle()
    w()
