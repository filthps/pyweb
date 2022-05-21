from rest_framework import pagination


class NotePaginator(pagination.PageNumberPagination):
    page_size = 2
    max_page_size = 3
