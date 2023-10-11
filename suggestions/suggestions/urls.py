"""
URL configuration for suggestions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from data import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.HomePage.as_view(), name='home'),
    path('phrases/', views.PhraseListView.as_view(),name='phrases'),
    path('phrases/form/', views.PhraseCreateView.as_view(),name='phrase_form'),
    path('phrases/<int:pk>/update/', views.PhraseUpdateView.as_view(), name='phrase_update'),
    path('phrases/<int:pk>/delete/', views.PhraseDeleteView.as_view(), name='phrase_delete'),
    path('phrases/<int:pk>', views.PhraselDetailView.as_view(),name='phrase_detail'),
    path('return_suggestions/', csrf_exempt(views.return_suggestions), name='return_suggestions'),
]
