from sqlmodel import (
    create_engine,
    SQLModel,
    Session,
    Field,
    Relationship,
)

"""Below code are starting to make my class for sqlmodel classes and so on"""

# faker library to generate the address & isbn number which i will use for practise
# https://faker.readthedocs.io/en/stable/providers/faker.providers.address.html
# https://faker.readthedocs.io/en/stable/providers/faker.providers.isbn.html


class Library(SQLModel, table=True):

    __tablename__ = "library_rana"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="NO Name Given")
    address: str = Field(default=None)
    owner_name: str

    books: list["Book"] = Relationship(back_populates="library")


class Book(SQLModel, table=True):

    __tablename__ = "book_table_rana"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    isbn: str
    author_name: str
    page_number: int
    price: float
    library_id: int | None = Field(default=None, foreign_key="library_rana.id")

    library: Library | None = Relationship(back_populates="books")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=0)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)







def main():
    create_db_and_tables()


if __name__ == "__main__":
    main()
