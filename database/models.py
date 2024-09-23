from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class ProductType(Base):

    __tablename__ = "product_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Product(Base):

    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    product_type_id: Mapped[int] = mapped_column(ForeignKey("product_type.id"))
