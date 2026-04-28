from django.urls import include, path
from rest_framework import routers
from document.api import views
from document.api.views import CategoryViewSet

router = routers.DefaultRouter()
router.register("user", views.UserViewSet)
router.register("note", views.NoteViewSet)
router.register("category", CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    ]