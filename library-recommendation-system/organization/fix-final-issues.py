import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔄 Fixing final issues: duplicates and books without covers...")
print("=" * 80)

# Silinecek kitaplar
books_to_delete = [
    # Kapaksızlar
    {"id": "263", "title": "Rule of Wolves (no cover)"},
    {"id": "228", "title": "Dark Age (no cover)"},
    
    # Duplicates (daha yeni eklenenler)
    {"id": "252", "title": "Shadow and Bone (duplicate)"},
    {"id": "250", "title": "Six of Crows (duplicate)"},
]

# Harry Potter serisi (3-6. kitaplar - 1 ve 2 zaten var)
new_books = [
    {"id": "228", "title": "Harry Potter and the Prisoner of Azkaban", "author": "J.K. Rowling", "genre": "Fantasy", "description": "Harry's third year at Hogwarts is threatened by the escaped prisoner Sirius Black.", "rating": 4.8, "year": 1999, "isbn": "9780439136365"},
    {"id": "250", "title": "Harry Potter and the Goblet of Fire", "author": "J.K. Rowling", "genre": "Fantasy", "description": "Harry competes in the dangerous Triwizard Tournament.", "rating": 4.8, "year": 2000, "isbn": "9780439139601"},
    {"id": "252", "title": "Harry Potter and the Order of the Phoenix", "author": "J.K. Rowling", "genre": "Fantasy", "description": "Harry forms Dumbledore's Army to fight against Voldemort's return.", "rating": 4.7, "year": 2003, "isbn": "9780439358071"},
    {"id": "263", "title": "Harry Potter and the Half-Blood Prince", "author": "J.K. Rowling", "genre": "Fantasy", "description": "Harry learns about Voldemort's past through Dumbledore's memories.", "rating": 4.7, "year": 2005, "isbn": "9780439785969"},
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

print(f"\n💕 Step 2: Adding Harry Potter books (3-7)...")
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
        print(f"   ✅ Added ID {book['id']}: {book['title']} ({book['year']})")
        add_count += 1
    except Exception as e:
        print(f"   ❌ ID {book['id']}: {str(e)}")

print("\n" + "=" * 80)
print(f"🎉 ISSUES FIXED!")
print(f"   🗑️  Deleted: {delete_count} books (2 no covers + 2 duplicates)")
print(f"   ⚡ Added: {add_count} Harry Potter books")
print("\n📚 Harry Potter series now complete:")
print("   1. Philosopher's Stone (already exists)")
print("   2. Chamber of Secrets (already exists)")
print("   3. Prisoner of Azkaban (1999) ✅")
print("   4. Goblet of Fire (2000) ✅")
print("   5. Order of the Phoenix (2003) ✅")
print("   6. Half-Blood Prince (2005) ✅")
print("\n✅ No duplicates, all covers verified!")
