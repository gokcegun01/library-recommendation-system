import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔄 Removing ALL duplicate books from DynamoDB...")
print("=" * 80)

# Tekrar eden kitapları sil (upload-books-part3.py'deki versiyonları)
duplicates_to_delete = [
    {"id": "215", "title": "Beloved"},
    {"id": "217", "title": "The Color Purple"},
    {"id": "223", "title": "The Bell Jar"},
    {"id": "228", "title": "Circe"},
    {"id": "246", "title": "The Fifth Season"},
    {"id": "250", "title": "Spinning Silver"},
    {"id": "251", "title": "Uprooted"},
    {"id": "252", "title": "The Hunger Games"},
    {"id": "258", "title": "The Night Circus"},
    {"id": "259", "title": "The Fault in Our Stars"},
    {"id": "260", "title": "The Ten Thousand Doors of January"},
    {"id": "263", "title": "The Invisible Life of Addie LaRue"},
    {"id": "283", "title": "The Perks of Being a Wallflower"},
    {"id": "287", "title": "The City of Brass"},
    {"id": "290", "title": "The Golem and the Jinni"},
]

# Yeni popüler kitaplar ekle
new_books = [
    {"id": "215", "title": "Red Rising", "author": "Pierce Brown", "genre": "Science Fiction", "description": "A lowborn miner infiltrates the elite to bring down their society from within.", "rating": 4.6, "year": 2014, "isbn": "978-0345539786"},
    {"id": "217", "title": "Morning Star", "author": "Pierce Brown", "genre": "Science Fiction", "description": "The third book in the Red Rising saga.", "rating": 4.7, "year": 2016, "isbn": "978-0345539809"},
    {"id": "223", "title": "Iron Gold", "author": "Pierce Brown", "genre": "Science Fiction", "description": "The fourth book in the Red Rising saga, set 10 years later.", "rating": 4.5, "year": 2018, "isbn": "978-0425285930"},
    {"id": "228", "title": "Dark Age", "author": "Pierce Brown", "genre": "Science Fiction", "description": "The fifth book in the Red Rising saga.", "rating": 4.8, "year": 2019, "isbn": "978-0425285954"},
    {"id": "246", "title": "Light Bringer", "author": "Pierce Brown", "genre": "Science Fiction", "description": "The sixth book in the Red Rising saga.", "rating": 4.7, "year": 2023, "isbn": "978-0593499832"},
    {"id": "250", "title": "Six of Crows", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "Six dangerous outcasts attempt an impossible heist.", "rating": 4.7, "year": 2015, "isbn": "978-1627792127"},
    {"id": "251", "title": "Crooked Kingdom", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "The sequel to Six of Crows.", "rating": 4.8, "year": 2016, "isbn": "978-1627792134"},
    {"id": "252", "title": "Shadow and Bone", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "An orphan discovers she has a unique magical power.", "rating": 4.4, "year": 2012, "isbn": "978-0805094596"},
    {"id": "258", "title": "Siege and Storm", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "The second book in the Shadow and Bone trilogy.", "rating": 4.3, "year": 2013, "isbn": "978-0805094602"},
    {"id": "259", "title": "Ruin and Rising", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "The final book in the Shadow and Bone trilogy.", "rating": 4.4, "year": 2014, "isbn": "978-0805094619"},
    {"id": "260", "title": "King of Scars", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "A young king fights the dark magic within him.", "rating": 4.5, "year": 2019, "isbn": "978-1510104464"},
    {"id": "263", "title": "Rule of Wolves", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "The sequel to King of Scars.", "rating": 4.6, "year": 2021, "isbn": "978-1510104471"},
    {"id": "283", "title": "Throne of Glass", "author": "Sarah J. Maas", "genre": "Fantasy", "description": "An assassin competes to become the king's champion.", "rating": 4.5, "year": 2012, "isbn": "978-1619630345"},
    {"id": "287", "title": "Crown of Midnight", "author": "Sarah J. Maas", "genre": "Fantasy", "description": "The second book in the Throne of Glass series.", "rating": 4.6, "year": 2013, "isbn": "978-1619630628"},
    {"id": "290", "title": "Heir of Fire", "author": "Sarah J. Maas", "genre": "Fantasy", "description": "The third book in the Throne of Glass series.", "rating": 4.7, "year": 2014, "isbn": "978-1619630659"},
]

print("\n🗑️  Step 1: Deleting duplicate books...")
delete_count = 0
for book in duplicates_to_delete:
    try:
        dynamodb.delete_item(
            TableName='Books',
            Key={'id': {'S': book['id']}}
        )
        print(f"   ✅ Deleted ID {book['id']}: {book['title']}")
        delete_count += 1
    except Exception as e:
        print(f"   ⚠️  ID {book['id']}: {str(e)}")

print(f"\n📚 Step 2: Adding new popular books...")
add_count = 0
for book in new_books:
    try:
        dynamodb.put_item(
            TableName='Books',
            Item={
                'id': {'S': book['id']},
                'title': {'S': book['title']},
                'author': {'S': book['author']},
                'genre': {'S': book['genre']},
                'description': {'S': book['description']},
                'rating': {'N': str(book['rating'])},
                'publishedYear': {'N': str(book['year'])},
                'isbn': {'S': book['isbn']},
                'coverImage': {'S': f"https://covers.openlibrary.org/b/isbn/{book['isbn']}-L.jpg"}
            }
        )
        print(f"   ✅ Added ID {book['id']}: {book['title']}")
        add_count += 1
    except Exception as e:
        print(f"   ❌ ID {book['id']}: {str(e)}")

print("\n" + "=" * 80)
print(f"🎉 Update complete!")
print(f"   🗑️  Deleted: {delete_count} duplicates")
print(f"   ✅ Added: {add_count} new books")
print("\n📚 Added popular series:")
print("   - Red Rising saga (Pierce Brown)")
print("   - Six of Crows duology (Leigh Bardugo)")
print("   - Shadow and Bone trilogy (Leigh Bardugo)")
print("   - King of Scars duology (Leigh Bardugo)")
print("   - Throne of Glass series (Sarah J. Maas)")
