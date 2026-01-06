#!/usr/bin/env python3
import boto3

# DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

# Books to delete (titles without cover images)
books_to_delete = [
    "Native Son",
    "Hell Bent",
    "The Queen of Nothing",
    "The Ruins",
    "The Kingdom of Copper",
    "Red Clocks",
    "The Fires of Vengeance",
    "The Girl Next Door",
    "A Torch Against the Night",
    "Me Before You",
    "The Time Traveler's Wife",
    "An Ember in the Ashes",
    "The Empire of Gold",
    "Crooked Kingdom",
    "The Spanish Love Deception",
    "The Dragon Republic",
    "The Seven Husbands of Evelyn Hugo",
    "The Poet",
    "The Snowman"
]

print(f"Searching for {len(books_to_delete)} books to delete...")

# Scan all books to find IDs
response = dynamodb.scan(TableName='Books')
all_books = response['Items']

# Continue scanning if there are more items
while 'LastEvaluatedKey' in response:
    response = dynamodb.scan(
        TableName='Books',
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    all_books.extend(response['Items'])

print(f"Found {len(all_books)} total books in database")

# Find books to delete
books_found = []
for book in all_books:
    title = book['title']['S']
    if title in books_to_delete:
        books_found.append({
            'id': book['id']['S'],
            'title': title
        })

print(f"\nFound {len(books_found)} books to delete:")
for book in books_found:
    print(f"  - ID {book['id']}: {book['title']}")

# Delete books
if books_found:
    confirm = input(f"\nDelete these {len(books_found)} books? (yes/no): ")
    if confirm.lower() == 'yes':
        deleted_count = 0
        for book in books_found:
            try:
                dynamodb.delete_item(
                    TableName='Books',
                    Key={'id': {'S': book['id']}}
                )
                print(f"✓ Deleted: {book['title']} (ID {book['id']})")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Error deleting {book['title']}: {e}")
        
        print(f"\n✓ Successfully deleted {deleted_count} books!")
    else:
        print("Deletion cancelled.")
else:
    print("\nNo books found to delete.")
