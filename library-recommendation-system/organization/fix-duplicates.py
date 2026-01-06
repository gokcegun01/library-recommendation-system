import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔄 Fixing duplicate books in DynamoDB...")
print("=" * 60)

# Books to update
updates = [
    {
        "id": "252",
        "old": "The Poppy War",
        "new": {
            "title": "The Hunger Games",
            "author": "Suzanne Collins",
            "genre": "Science Fiction",
            "description": "In a dystopian future, teens fight to the death in a televised event.",
            "rating": 4.6,
            "year": 2008,
            "isbn": "978-0439023481"
        }
    },
    {
        "id": "253",
        "old": "The Dragon Republic",
        "new": {
            "title": "Catching Fire",
            "author": "Suzanne Collins",
            "genre": "Science Fiction",
            "description": "The second book in the Hunger Games trilogy.",
            "rating": 4.6,
            "year": 2009,
            "isbn": "978-0439023498"
        }
    },
    {
        "id": "254",
        "old": "The Burning God",
        "new": {
            "title": "Mockingjay",
            "author": "Suzanne Collins",
            "genre": "Science Fiction",
            "description": "The final book in the Hunger Games trilogy.",
            "rating": 4.5,
            "year": 2010,
            "isbn": "978-0439023511"
        }
    },
    {
        "id": "259",
        "old": "The Starless Sea",
        "new": {
            "title": "The Fault in Our Stars",
            "author": "John Green",
            "genre": "Romance",
            "description": "Two teens with cancer fall in love.",
            "rating": 4.7,
            "year": 2012,
            "isbn": "978-0525478812"
        }
    },
    {
        "id": "264",
        "old": "Vicious",
        "new": {
            "title": "The Maze Runner",
            "author": "James Dashner",
            "genre": "Science Fiction",
            "description": "A boy wakes up in a maze with no memory of his past.",
            "rating": 4.3,
            "year": 2009,
            "isbn": "978-0385737951"
        }
    },
    {
        "id": "267",
        "old": "The Priory of the Orange Tree",
        "new": {
            "title": "Divergent",
            "author": "Veronica Roth",
            "genre": "Science Fiction",
            "description": "In a divided society, a girl discovers she doesn't fit into any faction.",
            "rating": 4.4,
            "year": 2011,
            "isbn": "978-0062024039"
        }
    },
    {
        "id": "283",
        "old": "The Rage of Dragons",
        "new": {
            "title": "The Perks of Being a Wallflower",
            "author": "Stephen Chbosky",
            "genre": "Fiction",
            "description": "A shy teenager navigates high school through letters.",
            "rating": 4.5,
            "year": 1999,
            "isbn": "978-0671027346"
        }
    }
]

success_count = 0
error_count = 0

for update in updates:
    try:
        print(f"\n📖 Updating ID {update['id']}: {update['old']} → {update['new']['title']}")
        
        # Delete old book
        dynamodb.delete_item(
            TableName='Books',
            Key={'id': {'S': update['id']}}
        )
        
        # Add new book
        dynamodb.put_item(
            TableName='Books',
            Item={
                'id': {'S': update['id']},
                'title': {'S': update['new']['title']},
                'author': {'S': update['new']['author']},
                'genre': {'S': update['new']['genre']},
                'description': {'S': update['new']['description']},
                'rating': {'N': str(update['new']['rating'])},
                'publishedYear': {'N': str(update['new']['year'])},
                'isbn': {'S': update['new']['isbn']},
                'coverImage': {'S': f"https://covers.openlibrary.org/b/isbn/{update['new']['isbn']}-L.jpg"}
            }
        )
        
        print(f"   ✅ Success!")
        success_count += 1
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        error_count += 1

print("\n" + "=" * 60)
print(f"🎉 Update complete!")
print(f"   ✅ Successful: {success_count}")
print(f"   ❌ Failed: {error_count}")
print("\n📚 Replaced duplicate books with popular 2000+ titles:")
print("   - The Hunger Games trilogy")
print("   - The Fault in Our Stars")
print("   - The Maze Runner")
print("   - Divergent")
print("   - The Perks of Being a Wallflower")
