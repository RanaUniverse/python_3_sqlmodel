from faker import Faker
import random

from sqlmodel import (
    create_engine,
    Field,  # type: ignore
    func,
    Relationship,
    select,
    Session,
    SQLModel,
)

"""Below code are starting to make my class for sqlmodel classes and so on"""

fake = Faker()


class Library(SQLModel, table=True):
    """
    This Library have name address and owner column
    """

    __tablename__: str = "library_rana"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str | None = Field(default=None)
    owner_name: str | None = None

    books: list["Book"] = Relationship(back_populates="library")

    def __repr__(self):
        return f"<Library(name={self.name}, address={self.address})>"


class Book(SQLModel, table=True):
    """
    This is a book class for testing, the isbn, page number,
    price, will be come from faker library
    """

    __tablename__: str = "book_rana"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    title: str
    isbn: str
    author_name: str
    page_number: int = Field(default=1, gt=0)
    price_in_inr: float = Field(default=1, ge=0)
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


def new_lib_and_book():
    """
    This will add a new library and a new book in the database.
    """
    two_word = (
        f"{fake.word('adjective')} "
        f"{fake.word('noun')} "
        f"{random.choice(["Book", "story","poem", "letter"])}"
    )
    with Session(engine) as session:
        lib_obj = Library(
            name=fake.company(),
            address=fake.address(),
            owner_name=fake.name(),
        )
        book_obj = Book(
            title=two_word,
            isbn=fake.isbn10(),
            author_name=fake.name_female(),
            library=lib_obj,
        )
        session.add(book_obj)
        session.commit()
        print(
            f"Library added: id={lib_obj.id}, name='{lib_obj.name}', owner_name='{lib_obj.owner_name}', address='{lib_obj.address}'\n"
            f"Book added: id={book_obj.id}, title='{book_obj.title}', isbn='{book_obj.isbn}', author_name='{book_obj.author_name}', "
            f"page_number={book_obj.page_number}, library_id={book_obj.library_id}, price_in_inr={book_obj.price_in_inr}\n"
            "Data committed successfully!"
        )


def get_library_by_name_old(name: str):
    """This fun dont work not match the case sensitivity"""
    with Session(engine) as session:
        statement = select(Library).where(Library.name == name)
        result = session.exec(statement)
        for lib in result:
            print(lib)


def get_library_by_name(name: str):
    with Session(engine) as session:
        statement = select(Library).where(func.lower(Library.name) == name.lower())
        result = session.exec(statement).all()
        if not result:
            print(f"No library found with name: '{name}'")
        for lib in result:
            print(lib)


def get_books_in_library(library_name: str):  # type: ignore
    with Session(engine) as session:
        statement = select(Library).where(
            func.lower(Library.name) == library_name.lower()
        )
        library_results = session.exec(statement).all()

        total_libs = len(library_results)
        print(f"Total libraries found: {total_libs}")

        if total_libs == 0:
            print(f"No library found with name: '{library_name}'")
            return

        for library_result in library_results:
            print(f"Library found: {library_result.name}")
            print(f"Books in '{library_result.name}':")
            if library_result.books:
                for book in library_result.books:
                    print(book)
            else:
                print("No books available in this library.")


def get_books_in_library(library_name: str):
    with Session(engine) as session:
        statement = select(Library).where(
            func.lower(Library.name) == library_name.lower()
        )
        library_results = session.exec(statement).all()

        total_libs = len(library_results)
        if total_libs < 0:
            print(f"Error: The number of libraries found is negative. ")
            return

        if total_libs == 0:
            print(f"No library found with name: '{library_name}'")
            return

        if total_libs == 1:
            library_result = library_results[0]
            print(f"Library found: {library_result.name}")
            print(f"Books in '{library_result.name}':")
            if library_result.books:
                for book in library_result.books:
                    print(book)
            else:
                print("No books available in this library.")

        elif total_libs > 1:
            print("Multiple libraries found with the given naME:")
            for library_result in library_results:
                print(f"\nLibrary found: {library_result.name}")
                print(f"Books in '{library_result.name}':")
                if library_result.books:
                    for book in library_result.books:
                        print(book)
                else:
                    print("No books available in this library.")
        print(f"Total libraries found: {total_libs}")


def main():
    create_db_and_tables()
    # get_library_by_name(name_of_lib)
    for _ in range(10):
        new_lib_and_book()
    # name_of_lib = "Davenport, Dunn and Anderson"
    # get_books_in_library(name_of_lib)


if __name__ == "__main__":
    main()
