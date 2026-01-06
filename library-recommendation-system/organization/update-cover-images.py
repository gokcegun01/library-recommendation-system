#!/usr/bin/env python3
import boto3
import time

dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

# Scan all books
response = dynamodb.scan(TableName='Books')
books = response.get('Items', [])

print(f"Found {len(books)} books to update")

# Update each book's cover image
for i, book in enumerate(books, 1):
    book_id = book['id']['S']
    isbn = book.get('isbn', {}).get('S', '')
    title = book.get('title', {}).get('S', 'Unknown')
    
    if isbn:
        # Remove hyphens from ISBN
        clean_isbn = isbn.replace('-', '')
        # Open Library Cover API - size L (large)
        cover_url = f"https://covers.openlibrary.org/b/isbn/{clean_isbn}-L.jpg"
        
        print(f"Updating {i}/{len(books)}: {title[:40]}... -> {cover_url}")
        
        try:
            dynamodb.update_item(
                TableName='Books',
                Key={'id': {'S': book_id}},
                UpdateExpression='SET coverImage = :cover',
                ExpressionAttributeValues={
                    ':cover': {'S': cover_url}
                }
            )
            time.sleep(0.1)  # Avoid throttling
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"Skipping {i}/{len(books)}: {title[:40]}... (no ISBN)")

print("\n✓ Cover images updated!")
