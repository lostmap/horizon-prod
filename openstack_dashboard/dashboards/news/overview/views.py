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
from horizon.decorators import require_perms, require_auth
import functools

from django.utils.decorators import available_attrs
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import redirect, render, get_object_or_404
#from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
#from django.urls import reverse
from openstack_dashboard import policy

#policy.check((("identity", "admin_required"),), request)
#context['create_network_allowed'] = policy.check((("network", "create_network"),), request)

@require_perms
def post_new(request):
    page_title = 'Create Post'
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = timezone.now()
            post.save()
            return redirect('horizon:news:overview:index')
    else:
        form = PostForm()
    return render(request, 'news/overview/edit.html', {'form': form, 'page_title': page_title})

@require_perms
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    page_title = post.title
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_date = timezone.now()
            post.save()
            return redirect('horizon:news:overview:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'news/overview/edit.html', {'post': post, 'form': form, 'page_title': page_title})

@require_perms
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('horizon:news:overview:index')


def post_list(request):
    admin_check = policy.check((("identity", "admin_required"),), request)
    page_title = 'Overview'
    posts = Post.objects.order_by('-created_date')
    return render(request, 'news/overview/index.html', {'posts': posts, 'page_title': page_title, 'admin': admin_check})

@require_perms
def post_detail(request, pk):
    admin_check = policy.check((("identity", "admin_required"),), request)
    post = get_object_or_404(Post, pk=pk)
    page_title = post.title
    return render(request, 'news/overview/detail.html', {'post': post, 'page_title': page_title, 'admin': admin_check})


class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'news/overview/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
