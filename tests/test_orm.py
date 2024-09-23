from database.models import Product, ProductType
from tests.conftest import async_session_maker
from sqlalchemy import select


async def test_get_types_name():
    async with async_session_maker() as session:
        stmt = select(ProductType)
        res = await session.execute(stmt)
        await session.commit()

    types = {}
    for i in res:
        key, value = i[0].id, i[0].name
        types.update({key: value})

    return types


async def test_insert_product(ac):

    async with async_session_maker() as session:

        session.add(Product(name="test_product", product_type_id=1))
        await session.commit()


async def test_select_all_products():

    types = await test_get_types_name()
    async with async_session_maker() as session:
        stmt = select(Product)
        res = await session.execute(stmt)
        await session.commit()

    return [{
        "id": i[0].id,
        "name": i[0].name,
        "product_type_id": types.get(i[0].product_type_id)
        }
        for i in res.all()
    ]
