from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('colours/', views.colours, name='colours'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.search, name='search'),
    path('mywardrobes/', views.get_requestor_orders, name='requestor_wardrobes'),
    # path('mywardrobes/<int:pk>', views.ProductByUserDetailView.as_view(), name='my_product'),
    path('mywardrobes/new', views.ProductByUserCreateView.as_view(), name='my_requested_new'),
    path('mywardrobes/<str:pk>', views.updateProductRequest, name='my_request_update'),
    path('my_request_delete/<str:pk>', views.deleteProductRequest, name='my_request_delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]


