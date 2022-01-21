from .kolatz import _3x_1

ROUNDS = 10_000

def mult(lst):
    n = 1
 
    for index, i in enumerate(lst):
        n *= (i + index)

    return n

def triple_slash(input_string, r=2):
    string_int = list(map(ord, input_string))
    number = mult(string_int)
    number += 1 if number % 2 == 0 else 0
    output = []

    main_result = _3x_1(number)

    for index, value in enumerate(string_int):
        if string_int.count(value) > 1:
            string_int[index] = value // (index + 1)

    for index, value in enumerate(string_int):
        if value % 2 == 0:
            string_int[index] = value + 1

    results = [_3x_1(i) for i in string_int]

    for index, result in enumerate(results):
        res = 0
        while True:
            try:
                res = (main_result[2][result[0]] // main_result[0])
                break
            except:
                result[0] //= 2

        for i in range(ROUNDS):
            if res == 0:
                res = result[0] // (index  + 1)
            
            if res < 33:
                res *= 1.5
            elif res > 126:
                res *= 0.5
        
        res = int(res)
        output.append(chr(res))

    return "".join(output)
