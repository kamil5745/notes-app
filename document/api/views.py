from document.models import View
from django.contrib.auth.models import User

from .pagination import NotePagination
from .permissions import IsOwner

from document.api.serializers import NoteSerializer, UserSerializer, LikeSerializer
from document.models import Note, Like

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = NotePagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'user__username']

    def get_queryset(self):
        queryset = Note.objects.all()

        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')

        if from_date:
            queryset = queryset.filter(created_at__date__gte=from_date)

        if to_date:
            queryset = queryset.filter(created_at__date__lte=to_date)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            if request.user.is_authenticated:
                self._handle_views(request.user, page)

            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _handle_views(self, user, notes):
        viewed_ids = View.objects.filter(user=user, note__in=notes).values_list('note_id', flat=True)
        new_views = [
            View(user=user, note=note)
            for note in notes if note.id not in viewed_ids
        ]
        if new_views:
            View.objects.bulk_create(new_views)

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        note = self.get_object()
        like_queryset = Like.objects.filter(user=request.user, note=note)

        if like_queryset.exists():
            like_queryset.delete()
            return Response({'liked': False}, status=status.HTTP_200_OK)
        else:
            Like.objects.create(user=request.user, note=note)
            return Response({'liked': True}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsOwner])
    def liked(self, request):
        liked_notes = Note.objects.filter(likes__user=request.user).distinct()
        liked_notes = self.filter_queryset(liked_notes)

        page = self.paginate_queryset(liked_notes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(liked_notes, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwner]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]