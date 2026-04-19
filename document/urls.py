from django.urls import path

from document.views import NoteCreateView, RegisterView, LoginView, LogoutView, NoteSingleView, \
    NoteFilterView, NoteLikeView, UserLikesView

urlpatterns = [
    path('', NoteFilterView.as_view(), name='list-view'),
    path('create/', NoteCreateView.as_view(), name='create-view'),
    path('likes/', UserLikesView.as_view(), name='likes-view'),
    path('<slug:slug>/', NoteSingleView.as_view(), name='single-view'),
    path('<slug:slug>/like/', NoteLikeView.as_view(), name='like-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
]
