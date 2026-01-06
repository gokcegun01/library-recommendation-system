#!/usr/bin/env python3
import json
import boto3
import time

# DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

# Read books data
with open('books-data-part2.json', 'r') as f:
    data = json.load(f)

books = data['Books']
print(f"Total books to upload: {len(books)}")

# Split into batches of 25 (DynamoDB limit)
batch_size = 25
batches = [books[i:i + batch_size] for i in range(0, len(books), batch_size)]

print(f"Split into {len(batches)} batches")

# Upload each batch
for i, batch in enumerate(batches, 1):
    print(f"\nUploading batch {i}/{len(batches)} ({len(batch)} items)...")
    
    try:
        response = dynamodb.batch_write_item(
            RequestItems={
                'Books': batch
            }
        )
        
        # Check for unprocessed items
        if response.get('UnprocessedItems'):
            print(f"  Warning: {len(response['UnprocessedItems'])} unprocessed items")
        else:
            print(f"  ✓ Batch {i} uploaded successfully")
        
        # Wait a bit to avoid throttling
        if i < len(batches):
            time.sleep(0.5)
            
    except Exception as e:
        print(f"  ✗ Error uploading batch {i}: {e}")

print("\n✓ Upload complete!")
