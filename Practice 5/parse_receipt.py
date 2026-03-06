import re
import json


def load_receipt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_prices(text):
    price_pattern = r'\d[\d\s]*,\d{2}'
    prices = re.findall(price_pattern, text)

    prices = [p.replace(" ", "") for p in prices]
    return prices


def extract_products(text):
    product_pattern = r'\d+\.\s*\n(.+?)\n\d'
    products = re.findall(product_pattern, text)

    return [p.strip() for p in products]


def extract_total(text):
    match = re.search(r'ИТОГО:\s*\n?([\d\s]+,\d{2})', text)
    if match:
        return match.group(1).replace(" ", "")
    return None


def extract_datetime(text):
    match = re.search(r'Время:\s*([\d\.]+\s[\d:]+)', text)
    if match:
        return match.group(1)
    return None


def extract_payment_method(text):
    match = re.search(r'(Банковская карта|Наличные)', text)
    if match:
        return match.group(1)
    return "Unknown"


def parse_receipt(file_path):
    text = load_receipt(file_path)

    data = {
        "products": extract_products(text),
        "prices": extract_prices(text),
        "total": extract_total(text),
        "datetime": extract_datetime(text),
        "payment_method": extract_payment_method(text)
    }

    return data


def main():
    receipt_data = parse_receipt("raw.txt")

    print(json.dumps(receipt_data, indent=4, ensure_ascii=False))


if name == "__main__":
    main()