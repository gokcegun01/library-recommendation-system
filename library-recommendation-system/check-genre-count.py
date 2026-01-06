#!/usr/bin/env python3
import boto3
from collections import Counter

dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

# Scan all books
response = dynamodb.scan(TableName='Books')
books = response.get('Items', [])

# Count by genre
genres = [book.get('genre', {}).get('S', 'Unknown') for book in books]
genre_counts = Counter(genres)

print(f"Total books: {len(books)}\n")
print("Genre distribution:")
for genre, count in sorted(genre_counts.items(), key=lambda x: x[1]):
    print(f"  {genre}: {count}")
