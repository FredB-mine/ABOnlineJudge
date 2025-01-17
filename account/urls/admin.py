try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from ..views.admin import UserAdminAPI, GenerateUserAPI

urlpatterns = [
    url(r"^user/?$", UserAdminAPI.as_view(), name="user_admin_api"),
    url(r"^generate_user/?$", GenerateUserAPI.as_view(), name="generate_user_api"),
]
