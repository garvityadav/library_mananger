from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    # post
    path('api/admin/signup', views.AdminSignupAPI.as_view(),
         name='api_admin_signup'),
    # post
    path('api/admin/login', views.AdminLoginAPI.as_view(),
         name='api_admin_login'),
    # post
    path('api/admin/logout', views.AdminLogoutAPI.as_view(),
         name='api_admin_logout'),
    # get
    path('api/books', views.books_api, name='api_books_list'),
    # post
    path('api/books/add', views.add_book_api, name='api_add_book'),
    path('api/books/update/<uuid:pk>',
         views.update_book_api, name='api_update_book'),
    path('api/books/delete/<uuid:pk>',
         views.delete_book_api, name='api_delete_book'),
    path('', views.student_view, name='student_view'),
]
