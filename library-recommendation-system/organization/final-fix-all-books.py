import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔄 FINAL FIX: Removing duplicates and books without covers...")
print("=" * 80)

# Silinecek kitaplar (tekrarlar + kapaksızlar)
books_to_delete = [
    # Tekrarlar
    {"id": "2", "title": "Project Hail Mary (duplicate)"},
    {"id": "133", "title": "The Night Circus (duplicate)"},
    {"id": "156", "title": "The Shining (duplicate)"},
    {"id": "171", "title": "Project Hail Mary (duplicate)"},
    {"id": "252", "title": "Shadow and Bone (duplicate)"},
    {"id": "250", "title": "Six of Crows (duplicate)"},
    
    # Kapaksızlar
    {"id": "221", "title": "Go Tell It on the Mountain (no cover)"},
    {"id": "228", "title": "Dark Age (no cover)"},
    {"id": "263", "title": "Rule of Wolves (no cover)"},
]

# Yeni popüler romantik kitaplar (2000+)
new_romance_books = [
    {"id": "2", "title": "The Hating Game", "author": "Sally Thorne", "genre": "Romance", "description": "Two executive assistants engage in a battle of wits and hearts.", "rating": 4.3, "year": 2016, "isbn": "978-0062439598"},
    {"id": "133", "title": "Red, White & Royal Blue", "author": "Casey McQuiston", "genre": "Romance", "description": "The son of the US President falls for a British prince.", "rating": 4.5, "year": 2019, "isbn": "978-1250316776"},
    {"id": "156", "title": "Beach Read", "author": "Emily Henry", "genre": "Romance", "description": "Two writers challenge each other to write in opposite genres.", "rating": 4.4, "year": 2020, "isbn": "978-1984806734"},
    {"id": "171", "title": "People We Meet on Vacation", "author": "Emily Henry", "genre": "Romance", "description": "Two best friends take one last trip together.", "rating": 4.5, "year": 2021, "isbn": "978-1984806758"},
    {"id": "221", "title": "The Love Hypothesis", "author": "Ali Hazelwood", "genre": "Romance", "description": "A PhD student fake-dates a professor.", "rating": 4.3, "year": 2021, "isbn": "978-0593336823"},
    {"id": "228", "title": "Book Lovers", "author": "Emily Henry", "genre": "Romance", "description": "A literary agent finds unexpected romance in a small town.", "rating": 4.4, "year": 2022, "isbn": "978-1984806772"},
    {"id": "250", "title": "The Spanish Love Deception", "author": "Elena Armas", "genre": "Romance", "description": "A woman needs a date for her sister's wedding in Spain.", "rating": 4.2, "year": 2021, "isbn": "978-1668003770"},
    {"id": "252", "title": "It Ends with Us", "author": "Colleen Hoover", "genre": "Romance", "description": "A woman must choose between her past and her future.", "rating": 4.6, "year": 2016, "isbn": "978-1501110368"},
    {"id": "263", "title": "Verity", "author": "Colleen Hoover", "genre": "Romance", "description": "A writer uncovers dark secrets while ghostwriting an autobiography.", "rating": 4.5, "year": 2018, "isbn": "978-1791392796"},
]

print("\n🗑️  Step 1: Deleting problematic books...")
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

print(f"\n💕 Step 2: Adding popular romance books (2000+)...")
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
print(f"🎉 FINAL FIX COMPLETE!")
print(f"   🗑️  Deleted: {delete_count} books")
print(f"   💕 Added: {add_count} romance books")
print("\n📚 Added popular romance authors:")
print("   - Emily Henry (Beach Read, People We Meet on Vacation, Book Lovers)")
print("   - Colleen Hoover (It Ends with Us, Verity)")
print("   - Sally Thorne (The Hating Game)")
print("   - Casey McQuiston (Red, White & Royal Blue)")
print("   - Ali Hazelwood (The Love Hypothesis)")
print("   - Elena Armas (The Spanish Love Deception)")
print("\n✅ All books are from 2016-2022, no duplicates!")
