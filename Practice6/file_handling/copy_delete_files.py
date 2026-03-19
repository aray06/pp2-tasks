import shutil
import os

# Копирование
shutil.copy("test.txt", "test_backup.txt")

# Удаление (безопасная проверка)
if os.path.exists("test_backup.txt"):
    os.remove("test_backup.txt")
    print("File deleted.")