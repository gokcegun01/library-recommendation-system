import requests
import time

print("🖼️  Checking cover images for new romance books...")
print("=" * 80)

# Yeni eklenen kitaplar
books = [
    {"id": "2", "title": "The Kiss Quotient", "isbn": "978-0451490803"},
    {"id": "133", "title": "The Bride Test", "isbn": "978-0451490827"},
    {"id": "156", "title": "The Heart Principle", "isbn": "978-0593336090"},
    {"id": "171", "title": "The Unhoneymooners", "isbn": "978-1501128035"},
    {"id": "221", "title": "The Flatshare", "isbn": "978-1250295675"},
    {"id": "228", "title": "The Switch", "isbn": "978-1250295699"},
    {"id": "250", "title": "Get a Life, Chloe Brown", "isbn": "978-0062941206"},
    {"id": "252", "title": "Take a Hint, Dani Brown", "isbn": "978-0062941213"},
    {"id": "263", "title": "Act Your Age, Eve Brown", "isbn": "978-0062941220"},
]

print("\n📚 Checking Open Library API for cover images...\n")

available = []
missing = []

for book in books:
    url = f"https://covers.openlibrary.org/b/isbn/{book['isbn']}-L.jpg"
    
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ ID {book['id']}: {book['title']}")
            print(f"   Cover: {url}")
            available.append(book)
        else:
            print(f"❌ ID {book['id']}: {book['title']}")
            print(f"   Status: {response.status_code}")
            missing.append(book)
    except Exception as e:
        print(f"❌ ID {book['id']}: {book['title']}")
        print(f"   Error: {str(e)}")
        missing.append(book)
    
    print()
    time.sleep(0.5)  # Be nice to the API

print("=" * 80)
print(f"\n📊 Summary:")
print(f"   ✅ Available covers: {len(available)}")
print(f"   ❌ Missing covers: {len(missing)}")

if missing:
    print(f"\n⚠️  Books without covers:")
    for book in missing:
        print(f"   - ID {book['id']}: {book['title']}")
    print("\n💡 These books will need to be replaced with books that have covers.")
else:
    print("\n🎉 All books have cover images!")
