from transduser import FinalTransducer
import itertools


def test():
    for i in range(1, 11):
        words_of_len_i = itertools.combinations_with_replacement('ab', i)
        for word in words_of_len_i:
            tr = FinalTransducer(8)
            word = ''.join(word)
            suffixes = generate_suffixes(word)
            answers = tr.get_words(word)
            assert not set(suffixes).intersection(set(answers))
    print("OK")


def generate_suffixes(word):
    word = word[::-1]
    for i in range(len(word)+1):
        yield word[:i][::-1]


def main():
    # test()
    print('Начальное состояние: ')
    tr = FinalTransducer(int(input()))
    print('Входное слово: ')
    input_word = input()
    out_put_words = set(tr.get_words(input_word))
    print('Результат: ')
    suffixes = set(generate_suffixes(input_word))
    for word in out_put_words:
        print(word)

    if not out_put_words.intersection(suffixes):
        print('В результате нет суффиксов входного слова')
    else:
        print('В результате есть суффиксы входного слова')


if __name__ == '__main__':
    main()
