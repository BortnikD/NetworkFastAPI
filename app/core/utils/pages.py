from app.core.config import BASE_URL


def get_prev_next_pages(offset: int, limit: int, count: int, path_name: str) -> tuple[str]:
    prev_offset = offset - limit if offset > 0 else None
    next_offset = offset + limit if offset + limit < count else None

    prev=f"{BASE_URL}/api/{path_name}?offset={prev_offset}&limit={limit}" if prev_offset is not None else None
    next=f"{BASE_URL}/api/{path_name}?offset={next_offset}&limit={limit}" if next_offset is not None else None

    return (prev, next)