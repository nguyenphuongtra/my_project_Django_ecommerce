from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/category/<int:category_id>/', views.product_list, name='product_list_by_category'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('review/<int:review_id>/vote/', views.vote_review, name='vote_review'),
    path('review/<int:review_id>/report/', views.report_review, name='report_review'),
]

