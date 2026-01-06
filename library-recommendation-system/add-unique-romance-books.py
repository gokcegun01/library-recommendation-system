import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔄 Replacing with UNIQUE romance books (not in system)...")
print("=" * 80)

# Şu an eklenen kitapları sil
books_to_delete = [
    {"id": "2", "title": "The Hating Game"},
    {"id": "133", "title": "Red, White & Royal Blue"},
    {"id": "156", "title": "Beach Read"},
    {"id": "171", "title": "People We Meet on Vacation"},
    {"id": "221", "title": "The Love Hypothesis"},
    {"id": "228", "title": "Book Lovers"},
    {"id": "250", "title": "The Spanish Love Deception"},
    {"id": "252", "title": "It Ends with Us"},
    {"id": "263", "title": "Verity"},
]

# Tamamen yeni, popüler romantik kitaplar (2000+)
new_romance_books = [
    {"id": "2", "title": "The Kiss Quotient", "author": "Helen Hoang", "genre": "Romance", "description": "A woman with Asperger's hires an escort to teach her about dating.", "rating": 4.4, "year": 2018, "isbn": "978-0451490803"},
    {"id": "133", "title": "The Bride Test", "author": "Helen Hoang", "genre": "Romance", "description": "A Vietnamese woman travels to America for an arranged marriage.", "rating": 4.5, "year": 2019, "isbn": "978-0451490827"},
    {"id": "156", "title": "The Heart Principle", "author": "Helen Hoang", "genre": "Romance", "description": "A violinist discovers herself through an unexpected romance.", "rating": 4.3, "year": 2021, "isbn": "978-0593336090"},
    {"id": "171", "title": "The Unhoneymooners", "author": "Christina Lauren", "genre": "Romance", "description": "Enemies are forced to pretend to be newlyweds on a honeymoon.", "rating": 4.4, "year": 2019, "isbn": "978-1501128035"},
    {"id": "221", "title": "The Flatshare", "author": "Beth O'Leary", "genre": "Romance", "description": "Two people share an apartment but have never met.", "rating": 4.3, "year": 2019, "isbn": "978-1250295675"},
    {"id": "228", "title": "The Switch", "author": "Beth O'Leary", "genre": "Romance", "description": "A grandmother and granddaughter swap lives for two months.", "rating": 4.2, "year": 2020, "isbn": "978-1250295699"},
    {"id": "250", "title": "Get a Life, Chloe Brown", "author": "Talia Hibbert", "genre": "Romance", "description": "A chronically ill woman makes a list to get a life.", "rating": 4.5, "year": 2019, "isbn": "978-0062941206"},
    {"id": "252", "title": "Take a Hint, Dani Brown", "author": "Talia Hibbert", "genre": "Romance", "description": "A fake relationship between a PhD student and a security guard.", "rating": 4.4, "year": 2020, "isbn": "978-0062941213"},
    {"id": "263", "title": "Act Your Age, Eve Brown", "author": "Talia Hibbert", "genre": "Romance", "description": "A free spirit crashes into the life of a uptight B&B owner.", "rating": 4.5, "year": 2021, "isbn": "978-0062941220"},
]

print("\n🗑️  Step 1: Deleting current books...")
delete_count = 0
for book in books_to_delete:
    try:
        dynamodb.delete_item(
            TableName='Books',
            Key={'id': {'S': book['id']}}
        )
        print(f"   ✅ Deleted ID {book['id']}: {book['title']}")
        delete_count += 1
    except Exception as e:
        print(f"   ⚠️  ID {book['id']}: {str(e)}")

print(f"\n💕 Step 2: Adding UNIQUE romance books...")
add_count = 0
for book in new_romance_books:
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
        print(f"   ✅ Added ID {book['id']}: {book['title']} ({book['year']})")
        add_count += 1
    except Exception as e:
        print(f"   ❌ ID {book['id']}: {str(e)}")

print("\n" + "=" * 80)
print(f"🎉 UNIQUE ROMANCE BOOKS ADDED!")
print(f"   🗑️  Deleted: {delete_count} books")
print(f"   💕 Added: {add_count} romance books")
print("\n📚 Added popular romance series:")
print("   Helen Hoang Series:")
print("   - The Kiss Quotient (2018)")
print("   - The Bride Test (2019)")
print("   - The Heart Principle (2021)")
print("\n   Beth O'Leary:")
print("   - The Flatshare (2019)")
print("   - The Switch (2020)")
print("\n   Talia Hibbert - Brown Sisters Series:")
print("   - Get a Life, Chloe Brown (2019)")
print("   - Take a Hint, Dani Brown (2020)")
print("   - Act Your Age, Eve Brown (2021)")
print("\n   Christina Lauren:")
print("   - The Unhoneymooners (2019)")
print("\n✅ All unique romance books, 2018-2021!")
