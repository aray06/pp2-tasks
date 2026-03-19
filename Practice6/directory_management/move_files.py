import shutil
import os

# Поиск файлов по расширению .txt и их перемещение
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(f"Found text file: {file}")