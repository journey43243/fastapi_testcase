from .core import engine_pg, session_var
from .models import Base, Product, ProductType
from sqlalchemy import select, insert, delete


async def create_tables() -> None:
    Base.metadata.create_all(engine_pg)


async def drop_tables() -> None:
    Base.metadata.drop_all(engine_pg)


async def create_products_type() -> None:

    async with session_var() as session:
        await session.execute(
            insert(ProductType).values([
                {"id": 1, "name": "trainers"},
                {"id": 2, "name": "jacket"},
                {"id": 3, "name": "socks"},
                {"id": 4, "name": "hats"}
            ]
            ))
        await session.commit()
        stmt = select(ProductType)
        await session.execute(stmt)
        await session.commit()

    return 'done'


async def select_all_products():

    types = await get_types_name()
    async with session_var() as session:
        stmt = select(Product)
        res = await session.execute(stmt)
        print(res)
        await session.commit()
        await session.close()

    return [{
        "id": i[0].id,
        "name": i[0].name,
        "product_type_id": types.get(i[0].product_type_id)
        }
        for i in res.all()
    ]


async def insert_product(product) -> Product:

    async with session_var() as session:
        if product.name != "test_product":
            session.add(Product(name=product.name,
                                product_type_id=product.product_type_id))
            await session.commit()
        else:
            stmt = delete(Product).where(Product.name == "test_product")
            await session.execute(stmt)
            await session.commit()

    return Product(name=product.name, product_type_id=product.product_type_id)


async def get_types_name() -> dict:

    hash_product_types = {}

    async with session_var() as session:

        stmt = select(ProductType)
        types = await session.execute(stmt)
        await session.commit()
        await session.close()

    for i in types.all():

        key = i[0].id
        value = i[0].name
        hash_product_types.update({key: value})

    return hash_product_types


async def get_product(product_id) -> Product:

    async with session_var() as session:

        stmt = select(Product).where(Product.id == int(product_id))
        product = await session.execute(stmt)
        await session.commit()
        await session.close()

    return product.first()[0] if product.first()[0] is not None else None


async def get_products_by_type(type_id) -> list:

    types = await get_types_name()

    async with session_var() as session:

        stmt = select(Product).where(Product.product_type_id == int(type_id))
        stmt_res = await session.execute(stmt)
        await session.commit()
        await session.close()

    products = [i[0] for i in stmt_res]

    return [{'id': i.id,
            'name': i.name,
             'product_type': types.get(i.product_type_id)} for i in products]
