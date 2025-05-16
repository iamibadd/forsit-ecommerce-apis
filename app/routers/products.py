from fastapi import APIRouter, Query, Path
from typing import Annotated
from app.dependencies import SessionDep, PaginationDep, UserDep
from app.crud import products as products_crud
from app.schemas.products import Product, ProductCategory, ProductCreate, ProductStatsMetric

router = APIRouter()


@router.get("", response_model=list[Product])
def get_products(
    db: SessionDep,
    pagination: PaginationDep,
    name: Annotated[str, Query(
        description="Filter by product name")] = None,
    description: Annotated[str, Query(
        description="Filter by product description")] = None,
):
    products = products_crud.get_products(
        db=db, pagination=pagination, name=name, description=description)
    return products


@router.post("", response_model=Product)
def create_product(
    db: SessionDep,
    authenticated_user: UserDep,
    product_data: ProductCreate,
):
    print(f'Product created by admin ${authenticated_user.email}')
    product = products_crud.create_product(db=db, product=product_data)
    return product


@router.get("/stats", summary="Get products stats", response_model=dict)
def get_product_stat(
    db: SessionDep,
    params: Annotated[ProductStatsMetric, Query(description="Filter by different metrics")],
):
    stats = products_crud.get_product_stat(db=db, params=params)
    return {params.metric: stats}


@router.get("/{product_id}", response_model=Product)
def get_product_by_id(
    db: SessionDep,
    product_id: Annotated[int, Path(description="Filter by product id")],
):
    product = products_crud.get_product_by_id(db=db, product_id=product_id)
    return product


@router.get("/category/{category_id}", response_model=list[ProductCategory])
def get_products_by_category(
    db: SessionDep,
    category_id: Annotated[int, Path(description="Filter by product id")],
    pagination: PaginationDep,
):
    product = products_crud.get_products_by_category(
        db=db, category_id=category_id, pagination=pagination)
    return product
