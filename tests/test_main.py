from tests.conftest import ac
from test_orm import test_select_all_products


async def test_get_products(ac: ac):

    client = ac
    await test_select_all_products()

    response = await client.get('/products')
    assert response.status_code == 200


async def test_get_products_post(ac: ac):

    client = ac
    response = await client.post('/products', json={'name': 'test_product',
                                                    "product_type_id": 1})
    assert response.json() == {
            "status_code": 200,
            "product": "test_product"
        }


async def test_get_product_per_id(ac: ac, id=1):

    client = ac
    response = await client.get(f'/products/{id}')

    assert response.status_code == 200


async def test_get_products_per_type_id(ac: ac):

    client = ac
    response = await client.get('/products/type/2')
    assert response.status_code == 200
