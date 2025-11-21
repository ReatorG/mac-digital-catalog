# backend/src/app/search/domain/search_service.py

from src.app.search.infrastructure.search_repository import SearchRepository

class SearchService:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    def search_artworks(self, query: str, page: int, page_size: int):
        results = self.repository.search_artworks(query)
        total = len(results)

        start = (page - 1) * page_size
        end = start + page_size

        return results[start:end], total

    def search_artists(self, query: str, page: int, page_size: int):
        results = self.repository.search_artists(query)
        total = len(results)

        start = (page - 1) * page_size
        end = start + page_size

        return results[start:end], total
