import json
import re


class WinJsonConverter:
    def __init__(self, rules={}):
        self.__rules: dict = rules.copy()

    def __validate_json(self):
        for key in self.__rules.keys():
            type_rules: dict = self.__rules[key].copy()

            for rule_item in type_rules.keys():
                if rule_item == "valide_foo":
                    template = re.findall("valid_[a-zA-Z]*", str(type_rules[rule_item]))

                    type_rules.update({"valide_foo": template[0]})
                    self.__rules.update({key: type_rules})

                elif rule_item == "do":
                    type_rules.update({"do": "do"})
                    self.__rules.update({key: type_rules})

                elif rule_item == "type":
                    type_rules.update({"type": "int"})
                    self.__rules.update({key: type_rules})

                elif rule_item == "available":
                    type_rules.update({"available": ["str"]})
                    self.__rules.update({key: type_rules})

        return self.__rules

    def write(self):
        with open("rules.json", "w") as file_:
            json.dump(self.__validate_json(), file_, indent=4)

    def read(self, rules_class):
        class_dict = rules_class.__dict__["_Rules__rules"]

        with open("rules.json", "r") as file_:
            data_: dict = json.load(file_)

            for key in class_dict.keys():
                data_[key]["valide_foo"] = class_dict[key]["valide_foo"]
                if key == "type_date":
                    data_[key]["do"] = class_dict[key]["do"]
                elif key == "type_int":
                    data_[key]["type"] = int
                elif key == "type_hidden":
                    data_[key]["available"] = [str]

            rules_class._Rules__rules = data_

            return data_
