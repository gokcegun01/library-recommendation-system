#!/usr/bin/env python3
import boto3

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb', region_name='eu-north-1')

# 90 NEW books (no duplicates from existing data)
famous_books = [
    {"id": "201", "title": "The Remains of the Day", "author": "Kazuo Ishiguro", "genre": "Fiction", "description": "A butler reflects on his life of service and missed opportunities for love.", "rating": 4.5, "year": 1989, "isbn": "978-0679731726"},
    {"id": "202", "title": "Never Let Me Go", "author": "Kazuo Ishiguro", "genre": "Science Fiction", "description": "A dystopian story about clones raised to donate their organs.", "rating": 4.4, "year": 2005, "isbn": "978-1400078776"},
    {"id": "203", "title": "The Goldfinch", "author": "Donna Tartt", "genre": "Fiction", "description": "A boy's life is changed forever after his mother dies in a museum bombing.", "rating": 4.3, "year": 2013, "isbn": "978-0316055437"},
    {"id": "204", "title": "The Secret History", "author": "Donna Tartt", "genre": "Mystery", "description": "A group of classics students at an elite college commit murder.", "rating": 4.5, "year": 1992, "isbn": "978-1400031702"},
    {"id": "205", "title": "Atonement", "author": "Ian McEwan", "genre": "Fiction", "description": "A young girl's lie destroys the lives of two lovers.", "rating": 4.4, "year": 2001, "isbn": "978-0385721790"},
    {"id": "206", "title": "Mrs. Dalloway", "author": "Virginia Woolf", "genre": "Fiction", "description": "A day in the life of a high-society woman in post-WWI England.", "rating": 4.2, "year": 1925, "isbn": "978-0156628709"},
    {"id": "207", "title": "Cloud Atlas", "author": "David Mitchell", "genre": "Science Fiction", "description": "Six interconnected stories spanning centuries.", "rating": 4.3, "year": 2004, "isbn": "978-0375507250"},
    {"id": "208", "title": "The Poisonwood Bible", "author": "Barbara Kingsolver", "genre": "Fiction", "description": "A missionary family's experience in the Belgian Congo.", "rating": 4.5, "year": 1998, "isbn": "978-0060786502"},
    {"id": "209", "title": "Middlesex", "author": "Jeffrey Eugenides", "genre": "Fiction", "description": "An intersex person's coming-of-age story spanning three generations.", "rating": 4.4, "year": 2002, "isbn": "978-0312422158"},
    {"id": "210", "title": "The Amazing Adventures of Kavalier & Clay", "author": "Michael Chabon", "genre": "Fiction", "description": "Two Jewish cousins create a comic book superhero during WWII.", "rating": 4.5, "year": 2000, "isbn": "978-0312282998"},
    {"id": "211", "title": "White Teeth", "author": "Zadie Smith", "genre": "Fiction", "description": "Two families navigate multicultural London.", "rating": 4.3, "year": 2000, "isbn": "978-0375703867"},
    {"id": "212", "title": "The Corrections", "author": "Jonathan Franzen", "genre": "Fiction", "description": "A Midwestern family struggles with modern life.", "rating": 4.2, "year": 2001, "isbn": "978-0312421717"},
    {"id": "213", "title": "Freedom", "author": "Jonathan Franzen", "genre": "Fiction", "description": "An American family's pursuit of happiness and freedom.", "rating": 4.3, "year": 2010, "isbn": "978-0312600846"},
    {"id": "214", "title": "The Brief Wondrous Life of Oscar Wao", "author": "Junot Díaz", "genre": "Fiction", "description": "A Dominican family's curse spans generations.", "rating": 4.4, "year": 2007, "isbn": "978-1594483295"},
    {"id": "215", "title": "Beloved", "author": "Toni Morrison", "genre": "Fiction", "description": "A former slave is haunted by her past.", "rating": 4.5, "year": 1987, "isbn": "978-1400033416"},
    {"id": "216", "title": "Song of Solomon", "author": "Toni Morrison", "genre": "Fiction", "description": "A man's quest to discover his family's past.", "rating": 4.4, "year": 1977, "isbn": "978-1400033423"},
    {"id": "217", "title": "The Color Purple", "author": "Alice Walker", "genre": "Fiction", "description": "An African American woman's journey to independence.", "rating": 4.6, "year": 1982, "isbn": "978-0156028356"},
    {"id": "218", "title": "Their Eyes Were Watching God", "author": "Zora Neale Hurston", "genre": "Fiction", "description": "A Black woman's journey through three marriages.", "rating": 4.5, "year": 1937, "isbn": "978-0060838676"},
    {"id": "219", "title": "Invisible Man", "author": "Ralph Ellison", "genre": "Fiction", "description": "A Black man's search for identity in America.", "rating": 4.4, "year": 1952, "isbn": "978-0679732761"},
    {"id": "220", "title": "Native Son", "author": "Richard Wright", "genre": "Fiction", "description": "A young Black man's life in 1930s Chicago.", "rating": 4.3, "year": 1940, "isbn": "978-0061148507"},
    {"id": "221", "title": "Go Tell It on the Mountain", "author": "James Baldwin", "genre": "Fiction", "description": "A young man's religious awakening in Harlem.", "rating": 4.4, "year": 1953, "isbn": "978-0345806567"},
    {"id": "222", "title": "Giovanni's Room", "author": "James Baldwin", "genre": "Fiction", "description": "An American man's affair with an Italian bartender in Paris.", "rating": 4.3, "year": 1956, "isbn": "978-0345806567"},
    {"id": "223", "title": "The Bell Jar", "author": "Sylvia Plath", "genre": "Fiction", "description": "A young woman's descent into mental illness.", "rating": 4.4, "year": 1963, "isbn": "978-0061148514"},
    {"id": "224", "title": "The Awakening", "author": "Kate Chopin", "genre": "Fiction", "description": "A woman's sexual and personal awakening in 1890s Louisiana.", "rating": 4.2, "year": 1899, "isbn": "978-0486277868"},
    {"id": "225", "title": "A Room of One's Own", "author": "Virginia Woolf", "genre": "Non-Fiction", "description": "An essay on women and fiction.", "rating": 4.5, "year": 1929, "isbn": "978-0156787338"},
    {"id": "226", "title": "The Testaments", "author": "Margaret Atwood", "genre": "Science Fiction", "description": "The sequel to The Handmaid's Tale, set 15 years later.", "rating": 4.3, "year": 2019, "isbn": "978-0385543781"},
    {"id": "227", "title": "Normal People", "author": "Sally Rooney", "genre": "Romance", "description": "The relationship between two Irish teenagers over several years.", "rating": 4.2, "year": 2018, "isbn": "978-1984822178"},
    {"id": "228", "title": "Circe", "author": "Madeline Miller", "genre": "Fantasy", "description": "The story of the witch Circe from Greek mythology.", "rating": 4.6, "year": 2018, "isbn": "978-0316556347"},
    {"id": "229", "title": "The Overstory", "author": "Richard Powers", "genre": "Fiction", "description": "Nine Americans whose lives are transformed by trees.", "rating": 4.3, "year": 2018, "isbn": "978-0393635522"},
    {"id": "230", "title": "There There", "author": "Tommy Orange", "genre": "Fiction", "description": "Urban Native Americans converge at the Big Oakland Powwow.", "rating": 4.4, "year": 2018, "isbn": "978-0525520375"},
    {"id": "231", "title": "The Water Dancer", "author": "Ta-Nehisi Coates", "genre": "Fiction", "description": "A slave with a mysterious power joins the Underground Railroad.", "rating": 4.2, "year": 2019, "isbn": "978-0399590597"},
    {"id": "232", "title": "The Vanishing Half", "author": "Brit Bennett", "genre": "Fiction", "description": "Twin sisters choose to live in very different worlds.", "rating": 4.5, "year": 2020, "isbn": "978-0525536291"},
    {"id": "233", "title": "Homegoing", "author": "Yaa Gyasi", "genre": "Fiction", "description": "Two half-sisters and their descendants across 300 years.", "rating": 4.6, "year": 2016, "isbn": "978-1101971062"},
    {"id": "234", "title": "Pachinko", "author": "Min Jin Lee", "genre": "Fiction", "description": "A Korean family's journey through four generations in Japan.", "rating": 4.5, "year": 2017, "isbn": "978-1455563937"},
    {"id": "235", "title": "The Underground Railroad", "author": "Colson Whitehead", "genre": "Fiction", "description": "A slave's journey to freedom on a literal underground railroad.", "rating": 4.4, "year": 2016, "isbn": "978-0385542364"},
    {"id": "236", "title": "The Nickel Boys", "author": "Colson Whitehead", "genre": "Fiction", "description": "Two boys at a brutal reform school in 1960s Florida.", "rating": 4.3, "year": 2019, "isbn": "978-0385537070"},
    {"id": "237", "title": "Lincoln in the Bardo", "author": "George Saunders", "genre": "Fiction", "description": "Abraham Lincoln mourns his son in a graveyard filled with ghosts.", "rating": 4.1, "year": 2017, "isbn": "978-0812995343"},
    {"id": "238", "title": "A Little Life", "author": "Hanya Yanagihara", "genre": "Fiction", "description": "Four college friends navigate life in New York City.", "rating": 4.3, "year": 2015, "isbn": "978-0804172707"},
    {"id": "239", "title": "The Luminaries", "author": "Eleanor Catton", "genre": "Mystery", "description": "A mystery set during the 1860s New Zealand gold rush.", "rating": 4.2, "year": 2013, "isbn": "978-0316074315"},
    {"id": "240", "title": "Wolf Hall", "author": "Hilary Mantel", "genre": "Fiction", "description": "Thomas Cromwell's rise to power in Henry VIII's court.", "rating": 4.3, "year": 2009, "isbn": "978-0312429980"},
    {"id": "241", "title": "Bring Up the Bodies", "author": "Hilary Mantel", "genre": "Fiction", "description": "The sequel to Wolf Hall about Anne Boleyn's downfall.", "rating": 4.4, "year": 2012, "isbn": "978-0805090031"},
    {"id": "242", "title": "The Mirror & the Light", "author": "Hilary Mantel", "genre": "Fiction", "description": "The final book in the Thomas Cromwell trilogy.", "rating": 4.5, "year": 2020, "isbn": "978-0805096606"},
    {"id": "243", "title": "The Essex Serpent", "author": "Sarah Perry", "genre": "Fiction", "description": "A widow investigates rumors of a mythical serpent in Victorian England.", "rating": 4.2, "year": 2016, "isbn": "978-0062666376"},
    {"id": "244", "title": "The Power", "author": "Naomi Alderman", "genre": "Science Fiction", "description": "Women develop the power to release electrical jolts.", "rating": 4.3, "year": 2016, "isbn": "978-0316547611"},
    {"id": "245", "title": "Red Clocks", "author": "Leni Zumas", "genre": "Science Fiction", "description": "Four women's lives in a world where abortion is illegal.", "rating": 4.1, "year": 2018, "isbn": "978-0316434195"},
    {"id": "246", "title": "The Fifth Season", "author": "N.K. Jemisin", "genre": "Fantasy", "description": "A woman searches for her daughter in a world of catastrophic climate change.", "rating": 4.5, "year": 2015, "isbn": "978-0316229296"},
    {"id": "247", "title": "The Obelisk Gate", "author": "N.K. Jemisin", "genre": "Fantasy", "description": "The second book in the Broken Earth trilogy.", "rating": 4.6, "year": 2016, "isbn": "978-0316229265"},
    {"id": "248", "title": "The Stone Sky", "author": "N.K. Jemisin", "genre": "Fantasy", "description": "The final book in the Broken Earth trilogy.", "rating": 4.7, "year": 2017, "isbn": "978-0316229241"},
    {"id": "249", "title": "The City We Became", "author": "N.K. Jemisin", "genre": "Fantasy", "description": "New York City comes alive to fight an ancient evil.", "rating": 4.3, "year": 2020, "isbn": "978-0316509848"},
    {"id": "250", "title": "Spinning Silver", "author": "Naomi Novik", "genre": "Fantasy", "description": "A retelling of Rumpelstiltskin with a Jewish moneylender's daughter.", "rating": 4.4, "year": 2018, "isbn": "978-0399180989"},
    {"id": "251", "title": "Uprooted", "author": "Naomi Novik", "genre": "Fantasy", "description": "A girl is taken by a wizard to live in his tower.", "rating": 4.5, "year": 2015, "isbn": "978-0804179034"},
    {"id": "252", "title": "The Poppy War", "author": "R.F. Kuang", "genre": "Fantasy", "description": "A war orphan discovers she has a powerful gift.", "rating": 4.5, "year": 2018, "isbn": "978-0062662569"},
    {"id": "253", "title": "The Dragon Republic", "author": "R.F. Kuang", "genre": "Fantasy", "description": "The second book in the Poppy War trilogy.", "rating": 4.6, "year": 2019, "isbn": "978-0062662606"},
    {"id": "254", "title": "The Burning God", "author": "R.F. Kuang", "genre": "Fantasy", "description": "The final book in the Poppy War trilogy.", "rating": 4.7, "year": 2020, "isbn": "978-0062662644"},
    {"id": "255", "title": "Babel", "author": "R.F. Kuang", "genre": "Fantasy", "description": "A dark academia novel about translation and colonialism.", "rating": 4.6, "year": 2022, "isbn": "978-0063021426"},
    {"id": "256", "title": "Piranesi", "author": "Susanna Clarke", "genre": "Fantasy", "description": "A man lives in a mysterious house with infinite rooms.", "rating": 4.4, "year": 2020, "isbn": "978-1635575637"},
    {"id": "257", "title": "Jonathan Strange & Mr Norrell", "author": "Susanna Clarke", "genre": "Fantasy", "description": "Two magicians bring magic back to 19th century England.", "rating": 4.3, "year": 2004, "isbn": "978-0765356154"},
    {"id": "258", "title": "The Night Circus", "author": "Erin Morgenstern", "genre": "Fantasy", "description": "Two magicians compete in a mysterious circus.", "rating": 4.5, "year": 2011, "isbn": "978-0307744432"},
    {"id": "259", "title": "The Starless Sea", "author": "Erin Morgenstern", "genre": "Fantasy", "description": "A graduate student discovers a mysterious underground library.", "rating": 4.2, "year": 2019, "isbn": "978-0385541213"},
    {"id": "260", "title": "The Ten Thousand Doors of January", "author": "Alix E. Harrow", "genre": "Fantasy", "description": "A girl discovers doors to other worlds.", "rating": 4.3, "year": 2019, "isbn": "978-0316421997"},
    {"id": "261", "title": "The Once and Future Witches", "author": "Alix E. Harrow", "genre": "Fantasy", "description": "Three sisters join the suffragists and bring back witchcraft.", "rating": 4.4, "year": 2020, "isbn": "978-0316422048"},
    {"id": "262", "title": "Mexican Gothic", "author": "Silvia Moreno-Garcia", "genre": "Horror", "description": "A woman investigates strange occurrences at a remote mansion.", "rating": 4.3, "year": 2020, "isbn": "978-0525620785"},
    {"id": "263", "title": "The Invisible Life of Addie LaRue", "author": "V.E. Schwab", "genre": "Fantasy", "description": "A woman makes a deal to live forever but be forgotten by everyone.", "rating": 4.5, "year": 2020, "isbn": "978-0765387561"},
    {"id": "264", "title": "Vicious", "author": "V.E. Schwab", "genre": "Fantasy", "description": "Two college roommates become archenemies with superpowers.", "rating": 4.4, "year": 2013, "isbn": "978-0765335340"},
    {"id": "265", "title": "Vengeful", "author": "V.E. Schwab", "genre": "Fantasy", "description": "The sequel to Vicious.", "rating": 4.3, "year": 2018, "isbn": "978-0765387530"},
    {"id": "266", "title": "A Darker Shade of Magic", "author": "V.E. Schwab", "genre": "Fantasy", "description": "A magician can travel between parallel Londons.", "rating": 4.4, "year": 2015, "isbn": "978-0765376459"},
    {"id": "267", "title": "The Priory of the Orange Tree", "author": "Samantha Shannon", "genre": "Fantasy", "description": "A standalone epic fantasy with dragons and political intrigue.", "rating": 4.3, "year": 2019, "isbn": "978-1635570298"},
    {"id": "268", "title": "The Bone Season", "author": "Samantha Shannon", "genre": "Fantasy", "description": "A clairvoyant criminal in a dystopian London.", "rating": 4.2, "year": 2013, "isbn": "978-1620401392"},
    {"id": "269", "title": "Ninth House", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "A girl with the ability to see ghosts attends Yale.", "rating": 4.3, "year": 2019, "isbn": "978-1250313072"},
    {"id": "270", "title": "Hell Bent", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "The sequel to Ninth House.", "rating": 4.4, "year": 2023, "isbn": "978-1250313096"},
    {"id": "271", "title": "Six of Crows", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "Six criminals attempt an impossible heist.", "rating": 4.6, "year": 2015, "isbn": "978-1627792127"},
    {"id": "272", "title": "Crooked Kingdom", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "The sequel to Six of Crows.", "rating": 4.7, "year": 2016, "isbn": "978-1627792158"},
    {"id": "273", "title": "Shadow and Bone", "author": "Leigh Bardugo", "genre": "Fantasy", "description": "An orphan discovers she has a unique magical power.", "rating": 4.3, "year": 2012, "isbn": "978-0805094596"},
    {"id": "274", "title": "The Cruel Prince", "author": "Holly Black", "genre": "Fantasy", "description": "A mortal girl navigates the treacherous world of faeries.", "rating": 4.4, "year": 2018, "isbn": "978-0316310277"},
    {"id": "275", "title": "The Wicked King", "author": "Holly Black", "genre": "Fantasy", "description": "The sequel to The Cruel Prince.", "rating": 4.5, "year": 2019, "isbn": "978-0316310314"},
    {"id": "276", "title": "The Queen of Nothing", "author": "Holly Black", "genre": "Fantasy", "description": "The final book in the Folk of the Air trilogy.", "rating": 4.6, "year": 2019, "isbn": "978-0316310369"},
    {"id": "277", "title": "An Ember in the Ashes", "author": "Sabaa Tahir", "genre": "Fantasy", "description": "A slave and a soldier in a brutal military empire.", "rating": 4.4, "year": 2015, "isbn": "978-1595148049"},
    {"id": "278", "title": "A Torch Against the Night", "author": "Sabaa Tahir", "genre": "Fantasy", "description": "The sequel to An Ember in the Ashes.", "rating": 4.5, "year": 2016, "isbn": "978-1595148063"},
    {"id": "279", "title": "Children of Blood and Bone", "author": "Tomi Adeyemi", "genre": "Fantasy", "description": "A girl fights to bring magic back to her land.", "rating": 4.3, "year": 2018, "isbn": "978-1250170972"},
    {"id": "280", "title": "Children of Virtue and Vengeance", "author": "Tomi Adeyemi", "genre": "Fantasy", "description": "The sequel to Children of Blood and Bone.", "rating": 4.2, "year": 2019, "isbn": "978-1250170996"},
    {"id": "281", "title": "Legendborn", "author": "Tracy Deonn", "genre": "Fantasy", "description": "A Black girl discovers a secret society of Arthurian legend.", "rating": 4.5, "year": 2020, "isbn": "978-1534441613"},
    {"id": "282", "title": "Bloodmarked", "author": "Tracy Deonn", "genre": "Fantasy", "description": "The sequel to Legendborn.", "rating": 4.6, "year": 2022, "isbn": "978-1534441637"},
    {"id": "283", "title": "The Rage of Dragons", "author": "Evan Winter", "genre": "Fantasy", "description": "A young man seeks revenge in a world at war.", "rating": 4.4, "year": 2019, "isbn": "978-0316489799"},
    {"id": "284", "title": "The Fires of Vengeance", "author": "Evan Winter", "genre": "Fantasy", "description": "The sequel to The Rage of Dragons.", "rating": 4.5, "year": 2020, "isbn": "978-0316489829"},
    {"id": "285", "title": "Black Leopard, Red Wolf", "author": "Marlon James", "genre": "Fantasy", "description": "An African fantasy epic about a mercenary tracker.", "rating": 4.1, "year": 2019, "isbn": "978-0735220171"},
    {"id": "286", "title": "Moon Witch, Spider King", "author": "Marlon James", "genre": "Fantasy", "description": "The sequel to Black Leopard, Red Wolf.", "rating": 4.2, "year": 2022, "isbn": "978-0735220188"},
    {"id": "287", "title": "The City of Brass", "author": "S.A. Chakraborty", "genre": "Fantasy", "description": "A con woman discovers she's part djinn.", "rating": 4.3, "year": 2017, "isbn": "978-0062678119"},
    {"id": "288", "title": "The Kingdom of Copper", "author": "S.A. Chakraborty", "genre": "Fantasy", "description": "The sequel to The City of Brass.", "rating": 4.4, "year": 2019, "isbn": "978-0062678157"},
    {"id": "289", "title": "The Empire of Gold", "author": "S.A. Chakraborty", "genre": "Fantasy", "description": "The final book in the Daevabad trilogy.", "rating": 4.5, "year": 2020, "isbn": "978-0062678195"},
    {"id": "290", "title": "The Golem and the Jinni", "author": "Helene Wecker", "genre": "Fantasy", "description": "A golem and a jinni form an unlikely friendship in 1899 New York.", "rating": 4.4, "year": 2013, "isbn": "978-0062110848"}
]

# Convert to DynamoDB format
def create_batch_write_requests(books):
    requests = []
    for book in books:
        # Clean title for cover image URL
        clean_title = book['title'].lower().replace(' ', '-').replace("'", '')
        cover_url = f"https://covers.openlibrary.org/b/isbn/{book['isbn']}-L.jpg"
        
        request = {
            "PutRequest": {
                "Item": {
                    "id": {"S": book["id"]},
                    "title": {"S": book["title"]},
                    "author": {"S": book["author"]},
                    "genre": {"S": book["genre"]},
                    "description": {"S": book["description"]},
                    "coverImage": {"S": cover_url},
                    "rating": {"N": str(book["rating"])},
                    "publishedYear": {"N": str(book["year"])},
                    "isbn": {"S": book["isbn"]}
                }
            }
        }
        requests.append(request)
    return requests

# Upload in batches of 25 (DynamoDB limit)
def upload_books():
    requests = create_batch_write_requests(famous_books)
    
    for i in range(0, len(requests), 25):
        batch = requests[i:i+25]
        try:
            response = dynamodb.batch_write_item(
                RequestItems={
                    'Books': batch
                }
            )
            print(f"Uploaded batch {i//25 + 1}: {len(batch)} books")
            
            # Handle unprocessed items
            if 'UnprocessedItems' in response and response['UnprocessedItems']:
                print(f"Warning: {len(response['UnprocessedItems'])} unprocessed items")
        except Exception as e:
            print(f"Error uploading batch {i//25 + 1}: {str(e)}")

if __name__ == "__main__":
    print(f"Starting upload of {len(famous_books)} famous books...")
    upload_books()
    print("Upload complete!")
