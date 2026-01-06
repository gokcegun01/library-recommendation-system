import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔄 Updating book: Replacing Mexican Gothic (ID 262) with Twilight...")

try:
    # Delete Mexican Gothic (ID 262)
    print("\n1️⃣ Deleting Mexican Gothic (ID 262)...")
    dynamodb.delete_item(
        TableName='Books',
        Key={'id': {'S': '262'}}
    )
    print("✅ Mexican Gothic deleted")
    
    # Add Twilight
    print("\n2️⃣ Adding Twilight (ID 262)...")
    dynamodb.put_item(
        TableName='Books',
        Item={
            'id': {'S': '262'},
            'title': {'S': 'Twilight'},
            'author': {'S': 'Stephenie Meyer'},
            'genre': {'S': 'Romance'},
            'description': {'S': 'A teenage girl falls in love with a vampire in the small town of Forks, Washington.'},
            'rating': {'N': '4.2'},
            'publishedYear': {'N': '2005'},
            'isbn': {'S': '978-0316015844'},
            'coverImage': {'S': 'https://covers.openlibrary.org/b/isbn/978-0316015844-L.jpg'}
        }
    )
    print("✅ Twilight added successfully!")
    
    print("\n🎉 Update complete! Mexican Gothic replaced with Twilight.")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
