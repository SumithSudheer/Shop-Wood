import pymongo

# Connect to the MongoDB client
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Get the "library" database
db = client["library"]

# Define the Books collection
books = db["books"]

# Define the Authors collection
authors = db["authors"]

# Create a sample author
author = {
    "name": "kasi",
    "nationality": "ind"
}

# Insert the author into the Authors collection
author_id = authors.insert_one(author).inserted_id
print(author_id,author_id)


# Create a sample book with a reference to the author
book = {
    "title": "the",
    "author": author_id
}

# Insert the book into the Books collection
books.insert_one(book)

# Query the Books collection for the book
book = books.find_one({"title": "the"})
print(book,"book")

# Use the author reference to retrieve the author from the Authors collection
author = authors.find_one({"_id": book["author"]})
print(author,'this is author')

# Print the author name
print(author["name"],"author[name]") # Output: John Doe

















# # verify.py
# from twilio.rest import Client

# def verify_phone_number(phone_number):
#     client = Client()

#     verification = client.verify.services('VA65074d1f5e116ff6216752199b738c04') \
#         .verifications \
#         .create(to='whatsapp:+{}'.format(phone_number), channel='whatsapp')

#     return verification.status
