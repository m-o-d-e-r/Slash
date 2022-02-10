from Slash.utilities.kolatz_utils.slash3_core import triple_slash
import string

mas = []

for i in string.ascii_letters:
    mas.append(triple_slash(f"hel{i}o"))

for i in mas:
    if mas.count(i) > 1:
        print(i)

