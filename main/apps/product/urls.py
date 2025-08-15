from django.urls import path
from . import views


urlpatterns = [
    path(
        "", 
        views.product_list_create_api_view,
        name='product_list_create'
    ),
    path(
        "<uuid:guid>/", 
        views.product_retrieve_update_delete_api_view, 
        name="product_detail_update_delete"
    ),
]


