import string
import sys


def is_digit(parameters):
    line_number = parameters['line_number']
    token = parameters['token']
    char = parameters['char']
    next_token = parameters['next_token']
    tokens_array = parameters['tokens_array']
    printLines = parameters['printLines']

    token += char

    if next_token in language_letters:
        print("erro")
    elif next_token not in language_digits:
        print_symbol(token, line_number, "constante inteira") if printLines else False
        tokens_array.append(token)

    return tokens_array, token


def is_letter(parameters):
    line_number = parameters['line_number']
    char = parameters['char']
    token = parameters['token']
    next_token = parameters['next_token']
    tokens_array = parameters['tokens_array']
    printLines = parameters['printLines']

    token += char

    if next_token not in language_letters:

        if token in language_words:
            print_symbol(token, line_number, "palavra reservada") if printLines else False
            tokens_array.append(token)
            token = ''
        else:
            print_symbol(token, line_number, "identificador") if printLines else False
            tokens_array.append(token)
            token = ''

    return tokens_array, token


def is_symbol(parameters):
    line_number = parameters['line_number']
    char = parameters['char']
    next_token = parameters['next_token']
    tokens_array = parameters['tokens_array']
    printLines = parameters['printLines']

    compose_symbol = True

    if next_token == "=" and char == ">":
        token_symbol = ">="
    elif next_token == "=" and char == "<":
        token_symbol = "<="
    elif next_token == "=" and char == "=":
        token_symbol = "=="
    elif next_token == "=" and char == "+":
        token_symbol = "+="
    elif next_token == "=" and char == "-":
        token_symbol = "-="
    else:
        compose_symbol = False
        token_symbol = char

    print_symbol(token_symbol, line_number, "simbolo especial") if printLines else False
    tokens_array.append(token_symbol)

    return tokens_array, compose_symbol


def split_token_from_array(text, printLines):

    tokens_array = []

    token = ''

    line_number = 0

    in_quotation_marks = False

    compose_symbol = False

    for line in text:
        line_number += 1

        if line[0] == "#":
            continue

        char_index = -1

        for char in line:

            char_index += 1

            if char.isspace():
                token = ''
                continue

            if compose_symbol:
                compose_symbol = False
                continue

            if char == "\"" and in_quotation_marks:
                print_symbol("\"", line_number, "simbolo especial") if printLines else False
                tokens_array.append("\"")
                in_quotation_marks = False

            elif char == "\"":
                print_symbol("\"", line_number, "simbolo especial") if printLines else False
                tokens_array.append("\"")
                in_quotation_marks = True

            if in_quotation_marks:
                continue

            if char_index + 1 < len(line):
                next_token = line[char_index + 1]
            else:
                next_token = " "

            parameters = {
                'token':        token,
                'char':         char,
                'next_token':   next_token,
                'tokens_array': tokens_array,
                'printLines':   printLines,
                'line_number':   line_number
            }

            if char in language_symbols:
                tokens_array, compose_symbol = is_symbol(parameters)
            elif char in language_letters:
                tokens_array, token = is_letter(parameters)
            elif char in language_digits:
                tokens_array, token = is_digit(parameters)


    file.close()
    return tokens_array


def print_symbol(token, line_nmb, type):
    print("linha", line_nmb, "|", type, token)


if __name__ == '__main__':

    syntactic_table = {
        "E": {
            "id": "ST",
            "num": "ST",
            "(": "ST",
        },
        "T": {
            "id": "GF",
            "num": "GF",
            "(": "GF",
        },
        "S": {
            "+": "ST+",
            "-": "ST-",
            ")": "VAZIO",
            "$": "VAZIO",
        },
        "G": {
            "+": "VAZIO",
            "-": "VAZIO",
            "*": "GF*",
            "/": "GF/",
            ")": "VAZIO",
            "$": "VAZIO",
        },
        "F": {
            "id": "id",
            "num": "num",
            "(": ")E(",
        }
    }

    rules = ["E", "T", "S", "G", "F"]
    language_symbols = ["[", "]", "<", ">", "<=", "+", ";", "=", "{", "}", "(", ")", "+", ".", "#", "%", ",", "-"]
    language_letters = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    language_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    language_words = ["main", "int", "float", "char", "printf", "if", "typedef", "void", "switch", "while",
                      "case", "break", "return", "puts", "scanf", "fopen", "FILE", "null", "exit", "gets"]

    file = open('c_code.txt', 'r')
    text = file.readlines()

    tokens_array = split_token_from_array(text, True)

    index_token = 0
    repeat = True
    tokens_array.append("$")
    stack = ["$", "E"]

    while repeat:
        current_token = tokens_array[0]
        stack_top = stack[-1]
        print("----------------------------------------------------------------------")
        print("PILHA  |", stack, "|")
        print("CADEIA |", tokens_array, "|")

        if stack_top not in rules or stack_top == "$":

            if stack_top == current_token:

                tokens_array.pop(0)
                stack.pop()
                if stack_top == "$":
                    print("Sucesso")
                else:
                    current_token = tokens_array[0]
            else:
                print("Erro")
                sys.exit()
        else:
            if current_token in syntactic_table[stack_top]:
                stack.pop()

                rule_value = syntactic_table[stack_top][current_token]
                print("REGRA  |", stack_top, "->", rule_value, "|")
                if rule_value == "VAZIO":
                    continue
                if stack_top == "F" and current_token != "(":

                    stack.append(rule_value)
                else:
                    rule_in_array = split_token_from_array(rule_value, False)

                    for token in rule_in_array:
                        stack.append(token)

            else:
                print("Erro")
                sys.exit()

        if stack_top == "$":
            repeat = False


