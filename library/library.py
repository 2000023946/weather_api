
class BookId:
    _book_id = 0

    @classmethod
    def generate_id(cls):
        cls._book_id +=1
        return cls._book_id
    
class Book:
    _number_books = 0
    __all_books = {}
    def __init__(self, author, title):
        self._author = author
        self._title = title
        __class__.all_books[title] =  __class__.all_books.get(title, 0) + 1
        __class__._number_books += 1
        self._book_id = BookId.generate_id()
    @classmethod
    def all_books(cls):
        return cls.__all_books

    @classmethod
    def get_number_books(cls):
        return cls._number_books

    def __str__(self):
        return f"Book Id: {self._book_id}. {self._title} by {self._author}."

class FictionBook(Book):
    _number_books = 0
    def __init__(self, author, title):
        __class__._number_books += 1
        super().__init__(author, title)

class NonFictionBook(Book):
    _number_books = 0
    def __init__(self, author, title):
        __class__._number_books += 1
        super().__init__(author, title)

class ReferenceBook(Book):
    _number_books = 0
    def __init__(self, author, title):
        __class__._number_books += 1
        super().__init__(author, title)

class TextBook(Book):
    _number_books = 0
    def __init__(self, author, title):
        __class__._number_books += 1
        super().__init__(author, title)

class Transaction:
    __all_transactions = []
    def __init__(self, user, book, duration):
        self.__user = user
        self.__book = book
        self.__time = duration
        __class__.__all_transactions.append(self)
    @staticmethod
    def borrow_book(title):
        book_dict = Book.all_books()
        if not title in book_dict['title']:
            return "Book not in stock"
        
    
    
    

harry1 = FictionBook(author="J.K Rowling", title="Philosopher's Stone")
harr2 = FictionBook(author="J.K Rowling", title="Philosopher's Stone")
ref1 = ReferenceBook(author="joe doe", title="Dict for French speakers")
text1 = TextBook(author="bob joe", title="AP US History")
non = NonFictionBook(author="bill nye", title="bees")

print(Book.all_books)
print(harry1.__dict__)
print(ref1.__dict__)
print(Book.get_number_books())
print(FictionBook.get_number_books())
print(NonFictionBook.get_number_books())
print(ReferenceBook.get_number_books())
print(TextBook.get_number_books())
    
