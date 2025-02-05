import json
from datetime import datetime

BOOKS_FILE = "books.json"
SALES_FILE = "sales.json"
USERS_FILE = "users.json"
CURRENT_USER_FILE = "current_user.json"

def load_data(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Login funksiyasi
def login():
    users = load_data(USERS_FILE)
    username = input("Username: ")

    user = next((u for u in users if u["username"] == username), None)
    if user:
        save_data(CURRENT_USER_FILE, user)
        print(f"Xush kelibsiz, {user['username']}!")
        return True
    else:
        print("Bunday foydalanuvchi mavjud emas!")
        return False

# Logout funksiyasi
def logout():
    save_data(CURRENT_USER_FILE, {})
    print("Tizimdan chiqildi!")

# Tizimga kim kirganini tekshirish
def get_current_user():
    user = load_data(CURRENT_USER_FILE)
    return user if user else None

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

# 2. Sotuv klassi
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

                        print(f"{user['username']} tomonidan '{book['title']}' kitob sotib olindi.")
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
        user = get_current_user()

        if not user:
            print("\n1. Kirish (Log in)")
            print("2. Dasturdan chiqish")
            choice = input("Tanlang: ")

            if choice == "1":
                login()
            elif choice == "2":
                break
            else:
                print("Noto‘g‘ri tanlov! Qaytadan urinib ko‘ring.")
        else:
            print(f"\nXush kelibsiz, {user['username']}!")
            print("1. Kitob qo‘shish")
            print("2. Kitoblarni ko‘rish")
            print("3. Kitob sotish")
            print("4. Sotuv tarixini ko‘rish")
            print("5. Chiqish (Log out)")

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
                book_id = int(input("Sotilayotgan kitob ID: "))
                Sale.sell(book_id, user["user_id"])

            elif choice == "4":
                Sale.view_all()

            elif choice == "5":
                logout()

            else:
                print("Noto‘g‘ri tanlov! Qaytadan urinib ko‘ring.")

if __name__ == "__main__":
    main()
