from collections import OrderedDict


class QuestionConverter:
    LIST_ITEM_FIELDS = ("id", "category", "type", "question", "complexity", "number_of_points", "max_attempts_to_solve")
    ITEM_DETAILS_FIELDS = LIST_ITEM_FIELDS + ("options",)

    def __init__(self):
        self.__field_mappers = {
            "id": self.__dummy_mapper("id"),
            "category": self.__category_mapper,
            "type": self.__dummy_mapper("type"),
            "question": self.__question_mapper,
            "complexity": self.__dummy_mapper("complexity"),
            "number_of_points": self.__dummy_mapper("number_of_points"),
            "max_attempts_to_solve": self.__dummy_mapper("max_attempts_to_solve"),
            "options": self.__options_mapper,
        }

    def __dummy_mapper(self, field_name):
        def mapper(question):
            return getattr(question, field_name)

        return mapper

    def __category_mapper(self, question):
        return OrderedDict((("id", question.category.id), ("name", question.category.name)))

    def __question_mapper(self, question):
        return question.text

    def __options_mapper(self, question):
        return [
            OrderedDict((("id", option.id), ("value", option.value)))
            for option in question.options.all()
        ]

    def to_list_item(self, question):
        return self.__convert(question, self.LIST_ITEM_FIELDS)

    def to_item_details(self, question):
        return self.__convert(question, self.ITEM_DETAILS_FIELDS)

    def __convert(self, question, fields):
        return OrderedDict([
            (field_name, self.__field_mappers[field_name](question))
            for field_name in fields
        ])
