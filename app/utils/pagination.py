from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from math import ceil


T = TypeVar('T')


class PaginationParams(BaseModel):
    """
    Standard pagination parameters for list endpoints.
    """
    page: int = 1
    page_size: int = 20
    
    @property
    def skip(self) -> int:
        """Calculate the number of records to skip."""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Get the page size limit."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.
    
    Provides consistent pagination metadata across all list endpoints.
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ) -> "PaginatedResponse[T]":
        """
        Create a paginated response.
        
        Args:
            items: List of items for current page
            total: Total number of items across all pages
            page: Current page number
            page_size: Number of items per page
            
        Returns:
            PaginatedResponse instance
        """
        total_pages = ceil(total / page_size) if page_size > 0 else 0
        
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
