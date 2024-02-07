from django.shortcuts import render, redirect
from django.views.generic import ListView
from .forms import KnowledgeForm
from .models import Knowledge

def index(request):
    return render(request, 'index.html')

def post_knowledge(request):
    if request.method == 'POST':
        form = KnowledgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = KnowledgeForm()

    return render(request, 'post_knowledge.html', {'form': form})

class KnowledgeListView(ListView):
    model = Knowledge
    template_name = "knowledge_list.html"
    context_object_name = "knowledges"