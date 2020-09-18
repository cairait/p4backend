from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import (
    ValidationError, PermissionDenied
)

from rest_framework.permissions import IsAuthenticated, AllowAny
from tasks.models import Category, Task
from tasks.serializers import CategorySerializer, TaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # list  categories per current loggedin user
        queryset = Category.objects.all().filter(owner=self.request.user)
        return queryset

    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        # check if category already exists for current logged in user
        category = Category.objects.filter(
            name=request.data.get('name'),
            owner=request.user
        )
        if category:
            msg = 'Category with that name already exists'
            raise ValidationError(msg)
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # user can only delete category he created
    def destroy(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs["pk"])
        if not request.user == category.owner:
            raise PermissionDenied("You can not delete this category")
        return super().destroy(request, *args, **kwargs)


class CategoryTasks(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        if self.kwargs.get("category_pk"):
            category = Category.objects.get(pk=self.kwargs["category_pk"])
            queryset = Task.objects.filter(
                owner=self.request.user,
                category=category
            )
            return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SingleCategoryTask(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):

        """
		kwargs = {
			"category_pk": 1,
			"pk": 1
		}
		"""
        if self.kwargs.get("category_pk") and self.kwargs.get("pk"):
            category = Category.objects.get(pk=self.kwargs["category_pk"])
            queryset = Task.objects.filter(
                pk=self.kwargs["pk"],
                owner=self.request.user,
                category=category)
            return queryset


class TasksViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all().filter(owner=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied(
                "Only logged in users with accounts can create tasks"
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs["pk"])
        if not request.user == task.owner:
            raise PermissionDenied(
                "You have no permissions to delete this task"
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs["pk"])
        if not request.user == task.owner:
            raise PermissionDenied(
                "You have no permissions to edit this task"
            )
        return super().update(request, *args, **kwargs)
