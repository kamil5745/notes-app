import datetime

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from document.models import Note, NoteFile, Category, Like
from django.core.validators import MinLengthValidator
import os


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class NoteFileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = NoteFile
        fields = ['id', 'file', 'name', 'url', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def get_name(self, obj):
        """Возвращает имя файла без пути"""
        return os.path.basename(obj.file.name)

    def get_url(self, obj):
        """Возвращает абсолютный URL файла"""
        return obj.file.url


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    name = serializers.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        error_messages={
            'min_length': 'Название должно содержать минимум 3 символа'
        }
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    files_upload = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=True,
        help_text="Список файлов для загрузки"
    )

    files = NoteFileSerializer(many=True, read_only=True)

    category_name = serializers.SerializerMethodField(read_only=True)

    likes_count = serializers.SerializerMethodField(read_only=True)

    isliked = serializers.SerializerMethodField(read_only=True)

    views_count = serializers.SerializerMethodField(read_only=True)

    date = serializers.DateField(required=False)

    class Meta:
        model = Note
        fields = [
            'id',
            'name',
            'description',
            'category',
            'category_name',
            'files',
            'files_upload',
            'created_at',
            'updated_at',
            'user',
            'likes_count',
            'isliked',
            'views_count',
            'date'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        files_to_upload = validated_data.pop('files_upload', [])

        likes = validated_data.pop('likes', None)

        note = Note.objects.create(**validated_data)

        if likes is not None:
            note.likes.set(likes)

        for file in files_to_upload:
            NoteFile.objects.create(note=note, file=file)

        return note

    def update(self, instance, validated_data):
        files_to_upload = validated_data.pop('files_upload', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for file in files_to_upload:
            NoteFile.objects.create(note=instance, file=file)

        return instance

    def get_user(self, obj):
        return obj.user.username

    def get_category_name(self, obj):
        return obj.category.name

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_isliked(self, obj):
        return obj.likes.filter(user=obj.user).exists()

    def get_views_count(self, obj):
        return obj.views.count()


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    note = NoteSerializer(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"