from fastapi import APIRouter, Query, Path
from typing import Annotated
from app.dependencies import SessionDep, PaginationDep, UserDep
from app.schemas.inventory import Inventory, InventoryUpdate
from app.schemas.inventory_history import InventoryHistory
from app.crud import inventory as inventory_crud
from app.crud import inventory_history as inventory_history_crud


router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("", response_model=list[Inventory])
def get_all_inventory_items(db: SessionDep, filter: PaginationDep):
    inventory = inventory_crud.get_all_inventory_items(db=db, filter=filter)
    return inventory


@router.get("/low-stock", response_model=list[Inventory])
def get_low_stock_items(db: SessionDep,
                        threshold: Annotated[int, Query(
        description="Enter threshold")] = 5):
    inventory = inventory_crud.get_low_stock_items(db=db, threshold=threshold)
    return inventory


@router.get("/product/{product_id}", response_model=Inventory)
def get_inventory_by_product(db: SessionDep,
                             product_id: Annotated[int, Path(
        description="Enter product id")]):
    inventory = inventory_crud.get_inventory_by_product(
        db=db, product_id=product_id)
    return inventory


@router.patch("/product/{product_id}", response_model=Inventory)
def update_product_inventory(db: SessionDep,
                             authenticated_user: UserDep,
                             product_id: Annotated[int, Path(
                                 description="Enter product id")],
                             inventory_data: InventoryUpdate):
    inventory = inventory_crud.update_product_inventory(
        db=db, product_id=product_id, inventory_data=inventory_data)
    print(f'Inventory updated by admin {authenticated_user.email}')
    return inventory


@router.get("/history", response_model=list[InventoryHistory])
def get_all_inventory_history(db: SessionDep, filter: PaginationDep):
    history = inventory_history_crud.get_all_inventory_history(
        db=db, filter=filter)
    return history


@router.get("/history/{inventory_id}", response_model=list[InventoryHistory])
def get_history_by_inventory(db: SessionDep,
                             inventory_id: Annotated[int, Path(
        description="Enter inventory id")]):
    inventory = inventory_history_crud.get_history_by_inventory(
        db=db, inventory_id=inventory_id)
    return inventory
