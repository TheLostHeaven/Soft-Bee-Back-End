from dataclasses import dataclass
from typing import Generic, List, Mapping, TypeVar

T = TypeVar("T")

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


@dataclass(frozen=True)
class PaginationParams:
    limit: int = DEFAULT_LIMIT
    offset: int = 0

    @classmethod
    def from_query_args(cls, args: Mapping[str, str]) -> "PaginationParams":
        """Parses and validates `limit` and `offset` from query string args.

        Raises ValueError with a user-facing message when values are invalid.
        """
        limit = cls._parse_int(args.get("limit"), "limit", DEFAULT_LIMIT)
        offset = cls._parse_int(args.get("offset"), "offset", 0)

        if limit < 1 or limit > MAX_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
        if offset < 0:
            raise ValueError("offset must be greater than or equal to 0")

        return cls(limit=limit, offset=offset)

    @staticmethod
    def _parse_int(raw, name: str, default: int) -> int:
        if raw is None or raw == "":
            return default
        try:
            return int(raw)
        except (TypeError, ValueError):
            raise ValueError(f"{name} must be an integer")


@dataclass(frozen=True)
class Page(Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int
