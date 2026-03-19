import os

# Создание вложенных папок
os.makedirs("parent/child", exist_ok=True)

# Список файлов и папок
print("Current directory content:", os.listdir("."))

# Текущая рабочая директория
print("Current path:", os.getcwd())