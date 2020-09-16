from rest_framework import serializers
from tasks.models import Category, Task


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = ('title', 'complete', 'created')


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    recipes = TaskSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Category
        fields = ('name', 'description')
