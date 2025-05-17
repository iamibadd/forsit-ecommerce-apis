from fastapi import HTTPException, status


def raise_not_found_if_empty(resource: str, resource_id: int, data: list | dict = None,  offset: int = 0):
    if not data and offset == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No {resource} found for {resource} ID {resource_id}"
        )
