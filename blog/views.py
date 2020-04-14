from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment

def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 9)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    comments = Comment.objects.filter(post=post)
    #общее количество коментариев к посту
    all_comment = comments.count()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                    'comments': comments,
                                                     'all_comment': all_comment })

def index(request):
    return render(request, 'blog/index.html')
