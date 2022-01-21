def _3x_1(number):
    y_range = [number]
    for count_or_rounds, i in enumerate(range(10_000)):
        if (number % 2) == 0:
            number //= 2
        else:
            number = number * 3 + 1
        y_range.append(number)

        if number == 1:
            return [count_or_rounds + 1, list(range(count_or_rounds + 2)), y_range]
