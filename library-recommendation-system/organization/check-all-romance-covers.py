import boto3
import urllib.request
import time

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔍 Scanning all Romance books in DynamoDB...")
print("=" * 80)

# Scan DynamoDB for Romance books
response = dynamodb.scan(
    TableName='Books',
    FilterExpression='genre = :genre',
    ExpressionAttributeValues={
        ':genre': {'S': 'Romance'}
    }
)

romance_books = response['Items']
print(f"\n📚 Found {len(romance_books)} Romance books\n")

books_without_covers = []
books_with_covers = []

for item in romance_books:
    book_id = item['id']['S']
    title = item['title']['S']
    cover_url = item.get('coverImage', {}).get('S', '')
    
    if not cover_url or cover_url == '':
        print(f"❌ ID {book_id}: {title}")
        print(f"   No cover URL")
        books_without_covers.append({'id': book_id, 'title': title})
        print()
        continue
    
    # Check if cover exists and is a real image (not placeholder)
    try:
        req = urllib.request.Request(cover_url)
        response = urllib.request.urlopen(req, timeout=5)
        data = response.read()
        
        # Check if image is too small (Open Library placeholder is ~807 bytes)
        if len(data) < 1000:
            print(f"❌ ID {book_id}: {title}")
            print(f"   Image too small ({len(data)} bytes) - likely placeholder")
            books_without_covers.append({'id': book_id, 'title': title, 'url': cover_url})
        else:
            print(f"✅ ID {book_id}: {title}")
            print(f"   Image size: {len(data)} bytes")
            books_with_covers.append({'id': book_id, 'title': title})
    except Exception as e:
        print(f"❌ ID {book_id}: {title}")
        print(f"   Error: {str(e)}")
        books_without_covers.append({'id': book_id, 'title': title, 'url': cover_url})
    
    print()
    time.sleep(0.3)

print("=" * 80)
print(f"\n📊 Summary:")
print(f"   ✅ Books with covers: {len(books_with_covers)}")
print(f"   ❌ Books without covers: {len(books_without_covers)}")

if books_without_covers:
    print(f"\n⚠️  Romance books without covers:")
    for book in books_without_covers:
        print(f"   - ID {book['id']}: {book['title']}")
    print("\n💡 These books need to be replaced!")
else:
    print("\n🎉 All Romance books have cover images!")
