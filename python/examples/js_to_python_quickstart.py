from dataclasses import dataclass
from pathlib import Path
import json

print('=== 1. 基础变量与字符串 ===')
name = 'Ada'
age = 18
print(f'{name} is {age} years old')

print('\n=== 2. 列表推导式（像 JS map/filter 的组合） ===')
numbers = [1, 2, 3, 4, 5, 6]
even_squares = [n * n for n in numbers if n % 2 == 0]
print(even_squares)

print('\n=== 3. dict 相当于更直接的数据对象 ===')
user = {'name': 'Ada', 'skills': ['Python', 'JavaScript'], 'active': True}
print(user['name'])
print(user.get('email', 'no-email'))

print('\n=== 4. for...of 风格循环 ===')
for index, skill in enumerate(user['skills'], start=1):
    print(index, skill)

print('\n=== 5. 函数：默认参数 + 关键字参数 ===')
def greet(name: str, prefix: str = 'Hi') -> str:
    return f'{prefix}, {name}'

print(greet('Ada'))
print(greet('Grace', prefix='Hello'))

print('\n=== 6. 类：优先学会 dataclass ===')
@dataclass
class Task:
    title: str
    done: bool = False

    def toggle(self) -> None:
        self.done = not self.done


task = Task('Write Python tutorial')
print(task)
task.toggle()
print(task)

print('\n=== 7. 文件与 pathlib ===')
output_dir = Path('python/examples/output')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / 'user.json'
output_file.write_text(json.dumps(user, ensure_ascii=False, indent=2), encoding='utf-8')
print(output_file)
print(output_file.read_text(encoding='utf-8'))

print('\n=== 8. 异常处理 ===')
raw_values = ['10', 'x', '30']
parsed = []
for value in raw_values:
    try:
        parsed.append(int(value))
    except ValueError:
        print(f'skip invalid integer: {value}')
print(parsed)

print('\n=== 9. 一个很 Python 的写法 ===')
prices = {'apple': 3, 'banana': 5, 'orange': 4}
total = sum(prices.values())
print(total)
