# name = 'Ada'
# age = 18 
# active = True
# print(f'{name} is {age}')

# def greet(name:str) ->str:
#     return f'Hello,{name}'
# print(greet('xsz'))

# numbers = [1,2,3]
# numbers.append(4)
# print(numbers[0])
# print(numbers[-1])

# user = {
#     'name':'Ada',
#     'age':18,
#     'skills':['Python','JavaScript']
# }

# print(user['name'])
# print(user.get('email'))
# print(user.get('email','no-email'))

# point = (10,20)
# skills = {'js','python','js'}
# print(skills)

# numbers = [1, 2, 3, 4, 5, 6]
# even_squares = [n * n for n in numbers if n % 2 ==0]
# print(even_squares)

# names = ['ada', 'grace', 'linus']
# upper_names = [name.upper() for name in names]
# print(upper_names)

# score = 75
# if score >=90:
#     print('A')
# elif score >=60:
#     print('B')
# else:
#     print('C')

# skills = ['js','python','sql']
# for skill in skills:
#     print(skill)

# for index,skill in enumerate(skills,start=1):
#     print(index,skill)

# count = 3
# while count >0 :
#     print(count)
#     count -=1

# def add(a,b):
#     return a +b
# def greet(name,prefix ='Hi'):
#     return f'{prefix},{name}'
# print(greet('Ada',prefix ='Hello'))

# def total(*numbers):
#     return sum(numbers)
# print(total(1,2,3))

# def print_user(**kwargs):
#     print(kwargs)
# print_user(name ='Ada',aget =18)

# class User:
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age

#     def greet(self):
#         return f'Hi, I am {self.name}'
# user = User('Ada',18)
# print(user.greet())

# from dataclasses import dataclass

# @dataclass
# class Task:
#     title:str
#     done:bool = False
    
#     def toggle(self):
#         self.done = not self.done

# task = Task('123')
# print(task.title)


# from math_tool import add
# print(add(1,2))

# from pathlib import Path
# file_path = Path('notes.txt')
# file_path.write_text('Hello, world!',encoding='utf-8')
# content = file_path.read_text(encoding='utf-8')
# print(content)

# try: 
#     n = int(value)
# except ValueError:
#     print('bad number')

def build_report(orders):
    paid_orders = [order for order in orders if order['paid']]
    total = sum(order['amount'] for order in paid_orders)
    names = [order['name'] for order in paid_orders]
    return {
        'count': len(paid_orders),
        'total': total, 
        'names': names
    }
orders = [
   {'name': 'book', 'amount': 30, 'paid': True},
    {'name': 'pen', 'amount': 10, 'paid': False},
    {'name': 'bag', 'amount': 80, 'paid': True},
]

print(build_report(orders))
