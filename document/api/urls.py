from django.urls import include, path
from rest_framework import routers
from document.api import views

router = routers.DefaultRouter()
router.register("user", views.UserViewSet)
router.register("note", views.NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]