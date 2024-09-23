from fastapi import FastAPI, APIRouter
import uvicorn
from .datamodels import ProductValidation
from database.orm import insert_product, select_all_products
from database.orm import get_types_name, get_product, get_products_by_type

app = FastAPI()
router = APIRouter()


@router.get("/products", tags=['products_id'],
            summary='Get all products',
            description='This endpoint return all products')
async def get_products():

    data = await select_all_products()

    return data


@router.post("/products", tags=['products_post'],
             summary='Create new products',
             description='This endpoint create new product')
async def get_products_post(product: ProductValidation):

    await insert_product(product=product)
    return {
        "status_code": 200,
        "product": product.name,
    }


@router.get("/products/{id}", tags=['product_item'],
            summary='Get product using type_id',
            description='This endpoint return product with defined id')
async def get_product_per_id(id):

    types = await get_types_name()
    product = await get_product(id)

    return {
        'id': product.id,
        'name': product.name,
        'product_type': types.get(product.product_type_id)
    }


@router.get("/products/type/{type_id}", tags=['product_type'],
            summary='Get products using product_type_id',
            description='This endpoint return products with defined \
                product_type_id')
async def get_products_per_type_id(type_id):

    products = await get_products_by_type(type_id)

    return products


app.include_router(router)


def start():
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
