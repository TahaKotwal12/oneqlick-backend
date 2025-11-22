from typing import List, Optional
from pydantic import BaseModel, Field

class RecentSearchResponse(BaseModel):
    """Response schema for a recent search"""
    search_query: str = Field(..., description="The search query")
    search_type: str = Field(..., description="Type of search (restaurant, food, general)")
    results_count: int = Field(..., description="Number of results found")
    created_at: str = Field(..., description="When the search was performed")

class RecentSearchesResponse(BaseModel):
    """Response schema for a list of recent searches"""
    recent_searches: List[RecentSearchResponse] = Field(..., description="List of recent searches")