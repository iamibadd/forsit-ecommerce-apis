from sqlalchemy.orm import Session

from app.schemas.helpers import Pagination
from app.schemas.inventory_history import InventoryHistoryCreate
from app.schemas.inventory import InventoryUpdate
from app.models import Inventory
from app.crud.inventory_history import create_history
from app.helpers.if_empty import raise_not_found_if_empty


def get_all_inventory_items(*, db: Session, filter: Pagination) -> list[Inventory]:
    return db.query(Inventory).offset(filter.offset).limit(filter.limit).all()


def get_low_stock_items(*, db: Session, threshold: int) -> list[Inventory]:
    return db.query(Inventory).filter(Inventory.quantity <= threshold).all()


def get_inventory_by_product(*, db: Session, product_id: int) -> Inventory:
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id).first()
    if not inventory:
        raise_not_found_if_empty('product', product_id)
    return inventory


def update_product_inventory(*, db: Session, product_id: int, inventory_data: InventoryUpdate) -> Inventory:
    inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id).first()
    if not inventory:
        raise_not_found_if_empty('product', product_id)

    new_quantity = inventory_data.new_quantity
    previous_quantity = inventory.quantity
    inventory.quantity = new_quantity
    inventory.product_id = product_id
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    history = InventoryHistoryCreate(
        inventory_id=inventory.id,
        previous_quantity=previous_quantity, new_quantity=new_quantity, description=inventory_data.description)
    create_history(db=db, history_data=history)
    return inventory
