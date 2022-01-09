from Slash.types_ import Rules, WinJsonConverter, JsonConverter


rule = Rules()
t = WinJsonConverter(rule.get_rules())
t.write()

#print(t.read(rule))
#print()
#print(rule.get_rules())