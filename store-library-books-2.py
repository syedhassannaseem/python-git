class library():
    def __init__(self):
        self.no_of_book= 0
        self.book= []
    def addbook(self,books):
        self.book.append(books)
        self.no_of_book = len(self.book)

    def showinfo(self):
        print(f"This library contain {self.no_of_book} books")
    def name_of_book(self):
        print(f"The name of the books that consist in library are \n {self.book}")
e=library()
e.addbook("harry potter")
e.showinfo()
e.name_of_book()