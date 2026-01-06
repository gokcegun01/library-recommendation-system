import boto3
import requests

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

def update_book_covers():
    """Update cover images for books 201-290 using Open Library API"""
    
    # Scan books with IDs 201-290
    response = dynamodb.scan(
        TableName='Books',
        FilterExpression='id BETWEEN :start AND :end',
        ExpressionAttributeValues={
            ':start': {'S': '201'},
            ':end': {'S': '290'}
        }
    )
    
    books = response['Items']
    print(f"Found {len(books)} books to update")
    
    updated_count = 0
    failed_count = 0
    
    for book in books:
        book_id = book['id']['S']
        isbn = book['isbn']['S']
        title = book['title']['S']
        
        # Try to get cover from Open Library
        cover_url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        
        try:
            # Check if cover exists
            response = requests.head(cover_url, timeout=5)
            if response.status_code == 200:
                # Update DynamoDB with cover URL
                dynamodb.update_item(
                    TableName='Books',
                    Key={'id': {'S': book_id}},
                    UpdateExpression='SET coverImage = :cover',
                    ExpressionAttributeValues={
                        ':cover': {'S': cover_url}
                    }
                )
                print(f"✓ Updated cover for: {title}")
                updated_count += 1
            else:
                print(f"✗ No cover found for: {title} (ISBN: {isbn})")
                failed_count += 1
        except Exception as e:
            print(f"✗ Error updating {title}: {str(e)}")
            failed_count += 1
    
    print(f"\nUpdate complete!")
    print(f"Successfully updated: {updated_count}")
    print(f"Failed: {failed_count}")

if __name__ == "__main__":
    print("Starting cover image update for books 201-290...")
    update_book_covers()
