from tkinter.filedialog import test
from Slash.types_ import triple_slash
import string

test_file = open("output_datas.txt", "a")

test_file.write(f"**********************************\n\n\n\n")

for test_item in string.ascii_letters:
    count = 0
    datas = []
    for i in string.ascii_letters:
        datas.append((f"{test_item}{i}{chr(ord(i) + 1)}", triple_slash(f"{test_item}{i}{chr(ord(i) + 1)}")))

    for ind1, i in enumerate(datas):
        for ind2, n in enumerate(datas):
            if ind1 != ind2 and i[1] == n[1]:
                #print(i, n)
                test_file.write(f"{i} {n}\n")
                count += 1

#    print(count)
    test_file.write(f"{count // 2}\n\n") if count != 0 else 0

test_file.close()
