from faker import Faker

from sqlmodel import (
    create_engine,
    SQLModel,
    Session,
    select,
    Field,
    Relationship,
)

"""Below code are starting to make my class for sqlmodel classes and so on"""

fake = Faker()


class Library(SQLModel, table=True):
    """
    This Library have name address and owner column
    """

    __tablename__ = "library_rana"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="No Name Given")
    address: str = Field(default=None)
    owner_name: str

    books: list["Book"] = Relationship(back_populates="library")

    def __repr__(self):
        return f"<Library(name={self.name}, address={self.address})>"


class Book(SQLModel, table=True):
    """
    This is a book class for testing, the isbn, page number,
    price, will be come from faker library
    """

    __tablename__ = "book_rana"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    isbn: str
    author_name: str
    page_number: int = Field(gt=0)
    price_in_inr: float = Field(ge=0)
    library_id: int | None = Field(default=None, foreign_key="library_rana.id")

    library: Library | None = Relationship(back_populates="books")

    def __repr__(self):
        return (
            f"<Book(title={self.title}, author={self.author_name}, isbn={self.isbn})>"
        )


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=0)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_books_in_central():
    """This is not use for now"""
    with Session(engine) as session:
        # Suppose Central Library is the default library first i will check if this library
        # Exists or not then create library first which is default library to insert book

        statement = select(Library).where(Library.name == "Central Library")
        library = session.exec(statement).first()

        if not library:
            library = Library(
                name="Central Library",
                address="123 Library Lane",
                owner_name="Rana Universe",
            )
            session.add(library)
            session.commit()

        book_math = Book(
            title="Geometry simple books",
            isbn=fake.isbn10(),
            author_name=fake.name(),
            page_number=100,
            price_in_inr=50,
            library_id=library.id,
        )

        session.add(book_math)
        session.commit()


def add_new_library_and_book(library_name: str = None):
    """
    Here i will add new library obj and a book in this library
    Later i will add the logic of library_name and owner name
    which i will check and use in the below code part.
    """
    two_word_name = fake.word("noun") + " " + fake.word("adjective")
    with Session(engine) as session:
        library_obj = Library(
            name=library_name, address=fake.address(), owner_name=fake.name()
        )
        session.add(library_obj)
        session.commit()

        book_obj = Book(
            title=two_word_name,
            author_name=fake.name_female(),
            isbn=fake.isbn10(),
            page_number=fake.random_int(100, 500, 5),
            price_in_inr=fake.random_int(99, 999, 10),
            library_id=library_obj.id,
        )
        session.add(book_obj)
        session.commit()


def main():
    create_db_and_tables()
    # create_books_in_central()
    add_new_library_and_book()
    for _ in range(1,10):
        lib_name = fake.word("noun")
        add_new_library_and_book(lib_name)
        print(f"{_}.) A New Library of name {lib_name} has been created")


if __name__ == "__main__":
    main()
