import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

print("🔄 Deleting duplicate Harry Potter and the Prisoner of Azkaban...")
print("=" * 80)

# ID 221'deki duplicate'i sil
try:
    dynamodb.delete_item(
        TableName='Books',
        Key={'id': {'S': '221'}}
    )
    print("✅ Deleted ID 221: Harry Potter and the Prisoner of Azkaban (duplicate)")
except Exception as e:
    print(f"❌ Error: {str(e)}")

# Yerine Harry Potter and the Deathly Hallows ekle
try:
    dynamodb.put_item(
        TableName='Books',
        Item={
            'id': {'S': '221'},
            'title': {'S': 'Harry Potter and the Deathly Hallows'},
            'author': {'S': 'J.K. Rowling'},
            'genre': {'S': 'Fantasy'},
            'description': {'S': 'The final battle between Harry and Voldemort. The epic conclusion to the Harry Potter series.'},
            'rating': {'N': '4.8'},
            'publishedYear': {'N': '2007'},
            'isbn': {'S': '9780545139700'},
            'coverImage': {'S': 'https://covers.openlibrary.org/b/isbn/9780545139700-L.jpg'}
        }
    )
    print("✅ Added ID 221: Harry Potter and the Deathly Hallows (2007)")
except Exception as e:
    print(f"❌ Error: {str(e)}")

print("\n" + "=" * 80)
print("🎉 DONE!")
print("\n📚 Harry Potter series now complete (1-7):")
print("   1. Philosopher's Stone")
print("   2. Chamber of Secrets")
print("   3. Prisoner of Azkaban (ID 228)")
print("   4. Goblet of Fire")
print("   5. Order of the Phoenix")
print("   6. Half-Blood Prince")
print("   7. Deathly Hallows (ID 221) ✅")
