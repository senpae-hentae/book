import json
from datetime import datetime

BOOKS_FILE = "books.json"
SALES_FILE = "sales.json"
USERS_FILE = "users.json"

def load_data(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 1. Kitob klassi
class Book:
    def __init__(self, title, author, genre, price, quantity):
        books = load_data(BOOKS_FILE)
        self.id = len(books) + 1
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.quantity = quantity

    def save(self):
        books = load_data(BOOKS_FILE)
        books.append(self.__dict__)
        save_data(BOOKS_FILE, books)
        print("Kitob qo'shildi!")

    def __str__(self):
        return f"{self.id}. {self.title} - {self.author} ({self.genre}) | {self.price} so‘m | {self.quantity} dona"

# 2. Foydalanuvchi klassi
class User:
    def __init__(self, username, address):
        users = load_data(USERS_FILE)
        self.user_id = len(users) + 1
        self.username = username
        self.address = address
        self.purchased_books = []

    def save(self):
        users = load_data(USERS_FILE)
        users.append(self.__dict__)
        save_data(USERS_FILE, users)
        print("Foydalanuvchi qo‘shildi!")

    def __str__(self):
        return f"ID: {self.user_id}, Username: {self.username}, Address: {self.address}"

# 3. Sotuv klassi
class Sale:
    @staticmethod
    def sell(book_id, user_id):
        books = load_data(BOOKS_FILE)
        sales = load_data(SALES_FILE)
        users = load_data(USERS_FILE)

        for book in books:
            if book["id"] == book_id and book["quantity"] > 0:
                for user in users:
                    if user["user_id"] == user_id:
                        sale = {
                            "book_id": book_id,
                            "user_id": user_id,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "price": book["price"]
                        }
                        sales.append(sale)
                        book["quantity"] -= 1
                        user["purchased_books"].append(book_id)

                        save_data(BOOKS_FILE, books)
                        save_data(SALES_FILE, sales)
                        save_data(USERS_FILE, users)

                        print(f"{user['username']} tomonidan '{book['title']}' sotib olindi.")
                        return
        print("Bu kitob mavjud emas yoki tugagan!")

    @staticmethod
    def view_all():
        sales = load_data(SALES_FILE)
        if not sales:
            print("Hech qanday sotuv amalga oshirilmagan!")
            return
        for sale in sales:
            print(f"Kitob ID: {sale['book_id']}, Foydalanuvchi ID: {sale['user_id']}, Sana: {sale['date']}, Narx: {sale['price']} so‘m")

def main():
    while True:
        print("\n1. Kitob qo‘shish")
        print("2. Kitoblarni ko‘rish")
        print("3. Foydalanuvchi qo‘shish")
        print("4. Kitob sotish")
        print("5. Sotuv tarixini ko‘rish")
        print("6. Chiqish")

        choice = input("Tanlang: ")

        if choice == "1":
            title = input("Kitob nomi: ")
            author = input("Muallif: ")
            genre = input("Janr: ")
            price = float(input("Narxi: "))
            quantity = int(input("Miqdori: "))
            Book(title, author, genre, price, quantity).save()

        elif choice == "2":
            books = load_data(BOOKS_FILE)
            if not books:
                print("Afsus, hech qanday kitob yo‘q!")
            else:
                for book in books:
                    print(f"ID: {book['id']}, {book['title']} - {book['author']} ({book['genre']}) | {book['price']} so‘m | Qolgan: {book['quantity']} dona")

        elif choice == "3":
            username = input("Foydalanuvchi ismi: ")
            address = input("Manzil: ")
            User(username, address).save()

        elif choice == "4":
            book_id = int(input("Sotilayotgan kitob ID: "))
            user_id = int(input("Foydalanuvchi ID: "))
            Sale.sell(book_id, user_id)

        elif choice == "5":
            Sale.view_all()

        elif choice == "6":
            break

        else:
            print("Noto‘g‘ri tanlov! Qaytadan urinib ko‘ring.")

if __name__ == "__main__":
    main()
