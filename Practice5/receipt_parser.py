import re
import json

def parse_receipt(text):
    # 1. Исправленный поиск цен: ищем только те, что в конце строки после стоимости
    # или те, что имеют формат цены (две цифры после запятой), игнорируя лишний мусор
    raw_prices = re.findall(r'(?<=Стоимость\n)([\d\s]*,\d{2})|(?<=\n)([\d\s]*,\d{2})(?=\n)', text)
    
    # Так как findall с группами возвращает кортежи, очищаем их
    prices_cleaned = []
    for p in raw_prices:
        val = p[0] if p[0] else p[1]
        prices_cleaned.append(float(val.replace(' ', '').replace(',', '.')))

    # 2. Названия продуктов (улучшенный поиск)
    products = re.findall(r'\d+\.\n(.*?)\n\d+,\d{3}\s+x', text, re.DOTALL)
    products = [p.strip().replace('\n', ' ') for p in products]

    # 3. Итоговая сумма
    total_match = re.search(r'ИТОГО:\n([\d\s]*,\d{2})', text)
    total_amount = float(total_match.group(1).replace(' ', '').replace(',', '.')) if total_match else 0.0

    # 4. Дата и время
    date_time_match = re.search(r'Время:\s+(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})', text)
    date = date_time_match.group(1) if date_time_match else None
    time = date_time_match.group(2) if date_time_match else None

    # 5. Способ оплаты
    payment_method = "Банковская карта" if "Банковская карта" in text else "Наличные"

    # Сборка финального JSON
    output = {
        "store": "EUROPHARMA",
        "date": date,
        "time": time,
        "payment_method": payment_method,
        "items": [],
        "total_amount": total_amount
    }

    # Ищем цены именно после слова "Стоимость", чтобы сопоставить с товарами
    item_costs_raw = re.findall(r'Стоимость\n([\d\s]*,\d{2})', text)
    
    for i in range(len(products)):
        if i < len(item_costs_raw):
            cost = float(item_costs_raw[i].replace(' ', '').replace(',', '.'))
            output["items"].append({
                "name": products[i],
                "price": cost
            })

    return output

# Чтение и запуск
try:
    with open('raw.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = parse_receipt(content)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    
    with open('receipt.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    print("\nГотово! Результат сохранен в receipt.json")
        
except Exception as e:
    print(f"Произошла ошибка: {e}")