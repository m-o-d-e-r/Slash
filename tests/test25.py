from Slash.types_ import (
    Int, Text, Bool, Date, Hidden, Email, Phone, IPv4, IPv6, Url,
    Rules
)

#  +    Int
#  +    Text
#  +    Bool
#  +    Date
#  +    Hidden
#  +    Email
#  +    Phone
#  +    IPv4
#  +    IPv6
#  +    Url

#print(Int(1)._is_valid_datas())
#print(Text("123")._is_valid_datas())
#print(Bool(123)._is_valid_datas())
#print(Date(Date.now())._is_valid_datas())
#print(Email("https://www.google.com/t-e_St=&")._is_valid_datas())
#print(Email("something.0@gmail.com")._is_valid_datas())
#print(Hidden(123)._is_valid_datas())
#print(Phone("+380000000000")._is_valid_datas())
#print(IPv4("127.0.0.1")._is_valid_datas())
#print(IPv6("2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d")._is_valid_datas())
#print(Url("https://www.google.com/t-e_St=&")._is_valid_datas())
