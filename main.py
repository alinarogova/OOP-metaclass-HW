from datetime import datetime

#Завдання 1
#Автоматичне додавання властивості
#Створіть метаклас, який автоматично додає властивість _creation_time до кожного
#створеного екземпляра класу. Значенням цієї властивості повинно бути час створення екземпляра.

class MetaClassAddProperty_creation_time(type):
    def __new__(cls, name, bases, class_dict):
        class_dict["_creation_time"] = datetime.now()

        return super().__new__(cls, name, bases, class_dict)
class MyClass(metaclass=MetaClassAddProperty_creation_time):
    pass

obj = MyClass()
print(obj._creation_time)

print("Task 2".center(40, "="))
#Створіть метаклас, який додає метод до кожного класу, створеного з його допомогою.
#Цей метод повинен повертати список всіх атрибутів і методів класу.
class AddMethodMeta(type):
    def __new__(cls, name, bases, class_dict):
        '''
        if 'get_attrs' not in class_dict:
            class_dict['get_attrs'] = lambda self: class_dict.keys()
        return super().__new__(cls, name, bases, class_dict)
        '''
        def get_attrs(self):
            return [attrs for attrs in dir(self) if attrs not in dir(type) and attrs!='get_attrs']

        class_dict['get_attrs'] = get_attrs

        return super().__new__(cls, name, bases, class_dict)


class MyClass(metaclass=AddMethodMeta):
    attrs = 0
    def __init__(self):
        self.attr1 = 0

    def Hello(self):
        pass

obj = MyClass()
print(obj.get_attrs())


print("Task 3".center(40, "="))
#Створіть метаклас, який забороняє змінювати значення атрибутів після створення екземпляра.
# Якщо атрибут вже встановлений, спроба змінити його значення повинна призводити до виключення

class ImmutableAttributesMeta(type):
    def __new__(cls, name, bases, class_dict):
        def setattr(self, value_name, value):
            if value_name in self.__dict__:
                raise AttributeError(f"{value_name} has already been in this class. You can't change a value.")
            super(self.__class__, self).__setattr__(value_name, value)

        class_dict["__setattr__"] = setattr

        return super().__new__(cls, name, bases, class_dict)

class MyClass3(metaclass=ImmutableAttributesMeta):
    def __init__(self, attr1, attr2):
        self.attr1 = attr1
        self.attr2 = attr2

obj3 = MyClass3(1, 2)
print(obj3.attr1)
obj3.attr3 = 6

print("Task 4".center(40, "="))
#Створіть метаклас, який обмежує наслідування від певного класу.
# Якщо новий клас намагається наслідувати клас, від якого наслідування заборонене, повинно підніматися виключення.

class NoInheritMeta(type):
    def __new__(cls, name, bases, class_dict):
        for base in bases:
            if isinstance(base, NoInheritMeta):
                raise TypeError(f"'{base.__name__}' can't have inherit.")
        return super().__new__(cls, name, bases, class_dict)

class Base(metaclass=NoInheritMeta):
    pass

try:
    class Inherit(Base):
        pass

except TypeError as e:
    print(e)