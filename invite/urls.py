"""vistor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from invite.apis import (
    InviteListApi,
    InviteDetailApi,
    InviteCreateApi,
    InviteUpdateApi,
    InviteStatusUpdateApi
)

urlpatterns = [
    path('', InviteListApi.as_view()),
    path('create/', InviteCreateApi.as_view()),
    path('<invite_id>/', InviteDetailApi.as_view()),
    path('<invite_id>/update/', InviteUpdateApi.as_view()),
    path('<invite_id>/status_update/', InviteStatusUpdateApi.as_view()),
]
