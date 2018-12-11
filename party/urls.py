from django.urls import path, re_path
from party import views
from django.conf import settings
from django.conf.urls.static import static

app_name='party'

urlpatterns = [
    # path('',views.PostListView.as_view(), name='party'),
    path('',views.post_list, name='party'),
    path('<int:pk>/',views.PostDetailView.as_view(), name='partydetail'),
    # path('<int:pk>/',views.CommentListView.as_view(), name='comment_display'),
    path('<int:pk>/',views.comment_display, name='commentlist'),
    path('create/', views.PostCreateView.as_view(), name='newparty'),
    path('about/',views.aboutTemplateView.as_view(), name='aboutpage'),
    re_path(r'by/(?P<username>[-\w]+)',views.UserPosts.as_view(),name='for_user'),
    path('delete/<int:pk>/', views.DeletePost.as_view(),name='delete'),
    path('<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)