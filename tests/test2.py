from Slash.types_ import triple_slash, Hidden


input_ = "password"

test = Hidden(input_)

output_ = test.value


print(input_)
print(output_)

print()


input_len = len(input_)
output_len = len(output_)

print(input_len)
print(output_len)


count = output_len // input_len

index_list = [i for i in range(0, len(output_), count)]
index_list.append(len(output_))

slice_list = []
for index, item in enumerate(index_list):
    if index == len(index_list) - 1:
        break
    slice_list.append((item, index_list[index + 1]))
                   
print()

data = [int(output_[i[0] : i[1]]) for i in slice_list]
print(data)


result = ""
for i in range(input_len):
    result += str(data[i] // ord(input_[i]) ** 2)

print(result)