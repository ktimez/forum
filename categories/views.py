from django.shortcuts import render , get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Topic, Reply
from django.contrib.auth.models import User
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView
from django.utils import timezone

def home(request):
    cats = Category.objects.all()
    return render(request, 'home.html', {'cats':cats })


def category_topics(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    topics = cat.topics.order_by('-last_updated').annotate(number_of_replies=Count('replies'))
    return render(request, 'topics.html', {'cat': cat, 'topics':topics})

@login_required
def new_topic(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    user = request.user #get the logged in User

    if request.method == 'POST':
        form = NewTopicForm(request.POST)
              
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = cat
            topic.starter = user
            topic.save()
            '''Reply.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )'''

            return redirect('topic_posts',pk=pk, topic_pk=topic.pk)

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'cat': cat, 'form':form})



def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)

    topic.views +=1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.created_by = request.user
            reply.save()


            reply.last_updated = timezone.now()  # <- here
            reply.save()                         # <- and here


            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Reply
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'topic_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.updated_by = self.request.user
        reply.updated_at = timezone.now()
        reply.save()
        return redirect('topic_posts', pk=reply.topic.category.pk, topic_pk=reply.topic.pk)