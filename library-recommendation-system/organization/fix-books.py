#!/usr/bin/env python3
import boto3
import time

dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

# Books to delete (problematic covers)
books_to_delete = [
    "The Spanish Love Deception",
    "The Poet", 
    "The Ruins",
    "Ring",
    "The Grip of It",
    "The Snowman"
]

print("Finding and deleting problematic books...")

# Scan to find these books
response = dynamodb.scan(TableName='Books')
books = response.get('Items', [])

deleted_count = 0
for book in books:
    title = book.get('title', {}).get('S', '')
    if title in books_to_delete:
        book_id = book['id']['S']
        print(f"Deleting: {title} (ID: {book_id})")
        dynamodb.delete_item(TableName='Books', Key={'id': {'S': book_id}})
        deleted_count += 1
        time.sleep(0.2)

print(f"\n✓ Deleted {deleted_count} books")

# Add replacement books
new_books = [
    # Non-Fiction (3 books)
    {
        'id': '201',
        'title': 'The Immortal Life of Henrietta Lacks',
        'author': 'Rebecca Skloot',
        'genre': 'Non-Fiction',
        'description': 'Her name was Henrietta Lacks, but scientists know her as HeLa. She was a poor black tobacco farmer whose cells—taken without her knowledge in 1951—became one of the most important tools in medicine.',
        'rating': 4.6,
        'publishedYear': 2010,
        'isbn': '978-1400052189'
    },
    {
        'id': '202',
        'title': 'Quiet: The Power of Introverts',
        'author': 'Susan Cain',
        'genre': 'Non-Fiction',
        'description': 'At least one-third of the people we know are introverts. They are the ones who prefer listening to speaking; who innovate and create but dislike self-promotion.',
        'rating': 4.5,
        'publishedYear': 2012,
        'isbn': '978-0307352156'
    },
    {
        'id': '203',
        'title': 'When Breath Becomes Air',
        'author': 'Paul Kalanithi',
        'genre': 'Non-Fiction',
        'description': 'At the age of thirty-six, on the verge of completing a decade of training as a neurosurgeon, Paul Kalanithi was diagnosed with stage IV lung cancer.',
        'rating': 4.7,
        'publishedYear': 2016,
        'isbn': '978-0812988406'
    },
    # Romance (3 books)
    {
        'id': '204',
        'title': 'The Wedding Date',
        'author': 'Jasmine Guillory',
        'genre': 'Romance',
        'description': 'A groomsman and his last-minute guest are about to discover if a fake date can go the distance in this fun and flirty multicultural romance.',
        'rating': 4.3,
        'publishedYear': 2018,
        'isbn': '978-0399587665'
    },
    {
        'id': '205',
        'title': 'The Unhoneymooners',
        'author': 'Christina Lauren',
        'genre': 'Romance',
        'description': 'Olive Torres is used to being the unlucky twin: from inexplicable mishaps to a recent layoff, her life seems to be almost comically jinxed.',
        'rating': 4.4,
        'publishedYear': 2019,
        'isbn': '978-1501128035'
    },
    {
        'id': '206',
        'title': 'The Simple Wild',
        'author': 'K.A. Tucker',
        'genre': 'Romance',
        'description': 'City girl Calla Fletcher attempts to reconnect with her estranged father, and unwittingly finds herself torn between her desire to return to the bustle of Toronto and a budding relationship with a rugged Alaskan pilot.',
        'rating': 4.5,
        'publishedYear': 2018,
        'isbn': '978-1501180569'
    }
]

print("\nAdding replacement books...")

for book in new_books:
    print(f"Adding: {book['title']}")
    
    # Convert to DynamoDB format
    item = {
        'id': {'S': book['id']},
        'title': {'S': book['title']},
        'author': {'S': book['author']},
        'genre': {'S': book['genre']},
        'description': {'S': book['description']},
        'coverImage': {'S': f"https://covers.openlibrary.org/b/isbn/{book['isbn'].replace('-', '')}-L.jpg"},
        'rating': {'N': str(book['rating'])},
        'publishedYear': {'N': str(book['publishedYear'])},
        'isbn': {'S': book['isbn']}
    }
    
    dynamodb.put_item(TableName='Books', Item=item)
    time.sleep(0.2)

print("\n✓ Replacement books added!")
print("\nNew distribution:")
print("  Non-Fiction: 15 + 3 = 18")
print("  Romance: 18 + 3 = 21")
print("  Horror: 56 - 6 = 50")
