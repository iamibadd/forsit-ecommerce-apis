from sqlalchemy.orm import Session

from app.schemas.helpers import Pagination
from app.schemas.inventory_history import InventoryHistoryCreate
from app.models import InventoryHistory
from app.helpers.if_empty import raise_not_found_if_empty


def create_history(*, db: Session, history_data: InventoryHistoryCreate) -> InventoryHistory:
    history = InventoryHistory.model_validate(history_data)
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def get_all_inventory_history(*, db: Session, filter: Pagination) -> list[InventoryHistory]:
    return db.query(InventoryHistory).offset(filter.offset).limit(filter.limit).all()


def get_history_by_inventory(*, db: Session, inventory_id: int) -> list[InventoryHistory]:
    history = db.query(InventoryHistory).filter(
        InventoryHistory.inventory_id == inventory_id).all()
    if not history:
        raise_not_found_if_empty('inventory', inventory_id)
    return history
