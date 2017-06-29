from colorama import Fore, Style
import sys

#https://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
class PrintInColor:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    @classmethod
    def red(cls, s, **kwargs):
        print(cls.RED + s + cls.END, **kwargs)

    @classmethod
    def green(cls, s, **kwargs):
        print(cls.GREEN + s + cls.END, **kwargs)

    @classmethod
    def yellow(cls, s, **kwargs):
        print(cls.YELLOW + s + cls.END, **kwargs)

    @classmethod
    def lightPurple(cls, s, **kwargs):
        print(cls.LIGHT_PURPLE + s + cls.END, **kwargs)

    @classmethod
    def purple(cls, s, **kwargs):
        print(cls.PURPLE + s + cls.END, **kwargs)


# https://stackoverflow.com/a/40426743/3222727
def get_pretty_table(iterable, header):
    header_output = get_pretty_header(iterable, header)
    content_output = get_pretty_table_content(iterable, header)
    return header_output + content_output


def get_pretty_header(iterable, header):
    max_len = [len(x) for x in header]
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        for index, col in enumerate(row):
            if max_len[index] < len(str(col)):
                max_len[index] = len(str(col))
    output = '-' * (sum(max_len) + 1) + '\n'
    output += '|' + ''.join([h + ' ' * (l - len(h)) + '|' for h, l in zip(header, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    return output


def get_pretty_table_content(iterable, header):
    max_len = [len(x) for x in header]
    output = ''
    for row in iterable:
        row = [row] if type(row) not in (list, tuple) else row
        output += '|' + ''.join([str(c) + ' ' * (l - len(str(c))) + '|' for c, l in zip(row, max_len)]) + '\n'
    output += '-' * (sum(max_len) + 1) + '\n'
    return output


def print_pretty_table(iterable, header):
    header_output = get_pretty_header(iterable, header)
    content_output = get_pretty_table_content(iterable, header)
    PrintInColor.green(header_output)
    print(content_output)


def main():
    PrintInColor.red('hello', end=' ')
    PrintInColor.green('world')
    print_pretty_table([[1, 2], [3, 4]], ['header 1', 'header 2'])


if __name__ == '__main__':
    main()
