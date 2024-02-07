from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post_knowledge', views.post_knowledge, name='post_knowledge'),
    path('knowledge_list', views.KnowledgeListView.as_view(), name='knowledge_list'),
]