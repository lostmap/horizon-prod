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

from django.conf.urls import url

from openstack_dashboard.dashboards.news.overview import views


urlpatterns = [
    url(r'^$', views.post_list, name='index'),
    url(r'^post/(?P<pk>\d+)$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete$', views.post_delete, name='post_delete'),
    url(r'^post/new$', views.post_new, name='post_new')
]
