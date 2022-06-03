from rest_framework import pagination


MAX_SIZE_NOTES = 16  # Максимальное количество notes в рамках одного запроса


class NotePaginator(pagination.PageNumberPagination):
    page_size = MAX_SIZE_NOTES - 1
    max_page_size = MAX_SIZE_NOTES
