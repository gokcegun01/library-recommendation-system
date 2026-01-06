import json

# Tüm kitap listelerini topla
all_books = []

# books-data.json'dan oku
print("📚 Reading books-data.json...")
with open('books-data.json', 'r') as f:
    data = json.load(f)
    for item in data['Books']:
        book_item = item['PutRequest']['Item']
        all_books.append({
            'id': book_item['id']['S'],
            'title': book_item['title']['S'],
            'source': 'books-data.json'
        })

# books-data-part2.json'dan oku
print("📚 Reading books-data-part2.json...")
with open('books-data-part2.json', 'r') as f:
    data = json.load(f)
    for item in data['Books']:
        book_item = item['PutRequest']['Item']
        all_books.append({
            'id': book_item['id']['S'],
            'title': book_item['title']['S'],
            'source': 'books-data-part2.json'
        })

# upload-books-part3.py'dan oku (manuel parse)
print("📚 Reading upload-books-part3.py...")
with open('upload-books-part3.py', 'r') as f:
    content = f.read()
    # Basit regex ile kitapları bul
    import re
    pattern = r'\{"id": "(\d+)", "title": "([^"]+)"'
    matches = re.findall(pattern, content)
    for match in matches:
        all_books.append({
            'id': match[0],
            'title': match[1],
            'source': 'upload-books-part3.py'
        })

print(f"\n📊 Total books found: {len(all_books)}")
print("=" * 80)

# Tekrarları bul
title_dict = {}
for book in all_books:
    title = book['title'].lower().strip()
    if title not in title_dict:
        title_dict[title] = []
    title_dict[title].append(book)

# Tekrar edenleri göster
duplicates = {title: books for title, books in title_dict.items() if len(books) > 1}

if duplicates:
    print(f"\n🔴 Found {len(duplicates)} duplicate titles:\n")
    for title, books in sorted(duplicates.items()):
        print(f"📖 {books[0]['title']}")
        for book in books:
            print(f"   - ID {book['id']} in {book['source']}")
        print()
else:
    print("\n✅ No duplicates found!")
