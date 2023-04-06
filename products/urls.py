from django.urls import path

from .views import (
    ProductListCreateView,
    ProductCategoryListCreateView, ProductListView, ProductUpdateView, ProductDeleteView
)

app_name = 'api'

urlpatterns = [

    path('', ProductListCreateView.as_view(), name='product_list_create'),
    path('update/<int:id>/', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<int:id>/', ProductDeleteView.as_view(), name='product_delete'),
    path('all/',ProductListView.as_view(), name='product_list_all'),
    path('details/id=<int:id>/',ProductListView.as_view(), name='product_detail_by_id'),
    path('details/name=<str:name>/', ProductListView.as_view(), name='product_detail_by_name'),
    path('product-categories/', ProductCategoryListCreateView.as_view(), name='product_category_list'),

]
