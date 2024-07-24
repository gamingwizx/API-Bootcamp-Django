from rest_framework import pagination

class StandardResultSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_query_param = "p"
    max_page_size = 2
    page_size_query_param = "size"