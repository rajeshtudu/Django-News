from blog_app.models import Tag, Category, Post
from django.utils import timezone
from datetime import timedelta


def navigation(request):

    one_week_ago = timezone.now() - timedelta(days=7)

    categories = Category.objects.all()[:5]
    tags = Tag.objects.all()[:5]
    recent_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-published_at")[:5]
    most_viewed = (
        Post.objects.filter(published_at__isnull=False, status="active")
        .order_by("-views_count")
        .first()
    )
    top_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("-views_count")[:3]
    weekly_posts = Post.objects.filter(
        published_at__isnull=False, status="active", published_at__gte=one_week_ago
    ).order_by("-views_count")[:5]
    random_posts = Post.objects.filter(
        published_at__isnull=False, status="active"
    ).order_by("?")[:5]
    return {
        "categories": categories,
        "tags": tags,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "most_viewed": most_viewed,
        "weekly_posts": weekly_posts,
        "random_posts": random_posts,
    }
