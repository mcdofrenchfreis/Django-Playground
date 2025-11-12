"""DRF serializers for todoapp."""
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Todo
        fields = [
            'id',
            'owner',
            'owner_username',
            'title',
            'description',
            'completed',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'owner', 'owner_username', 'created_at', 'updated_at']
