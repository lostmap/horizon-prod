# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from horizon import views
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = timezone.now()
            post.save()
            return redirect('horizon:news:overview:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'news/overview/edit.html', {'form': form})

def post_list(request):
    page_title = 'Overview'
    posts = Post.objects.order_by('-created_date')
    return render(request, 'news/overview/index.html', {'posts': posts, 'page_title': page_title})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    page_title = post.title
    return render(request, 'news/overview/detail.html', {'post': post, 'page_title': page_title})


class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'news/overview/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
