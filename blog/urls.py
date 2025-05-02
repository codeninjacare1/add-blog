from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    path('post_list', views.BlogPostListView.as_view(), name='post_list'),
    path('my-posts/', views.MyPostsView.as_view(), name='my_posts'),
    path('post/<int:pk>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.BlogPostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.BlogPostDeleteView.as_view(), name='post_delete'),
    path('pending-posts/', views.PendingPostsView.as_view(), name='pending_posts'),
    path('post/<int:pk>/approve/', views.approve_post, name='approve_post'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Authentication URLs
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
        next_page='blog:post_list'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:post_list'), name='logout'),
    
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
] 