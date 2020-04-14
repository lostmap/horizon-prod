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
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.order_by('-created_date')
    return render(request, 'news/overview/index.html', {'posts': posts})

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'news/overview/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return context
