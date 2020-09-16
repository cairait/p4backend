from django.urls import path, include
from . import views
from django.conf.urls import url
from rest_framework import routers
from tasks.views import CategoryViewSet, CategoryTasks, SingleCategoryTask, TasksViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('tasks', TasksViewSet, basename='task')

# urlpatterns = [
#     path('', views.index, name="list"),
#     path('update_task/<str:pk>/', views.updateTask, name="update_task"),
#     path('delete/<str:pk>/', views.deleteTask, name="delete"),
# ]

custom_urlpatterns = [
    url(r'categories/(?P<category_pk>\d+)/recipes$', CategoryTasks.as_view(), name='category_tasks'),
    url(r'categories/(?P<category_pk>\d+)/recipes/(?P<pk>\d+)$', SingleCategoryTask.as_view(),
        name='single_category_task'),
]

urlpatterns = router.urls
urlpatterns += custom_urlpatterns

# urlpatterns = [
# 	path('', include(router.urls))
# ]
