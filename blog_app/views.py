from datetime import timedelta

from django.conf import settings as conf_settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
    TemplateView,
)
from django.contrib import messages
from blog_app.forms import CommentForm, ContactForm, NewsLetterForm, PostForm
from blog_app.models import Category, Post, Tag

paginate_by = conf_settings.PAGINATE_BY

one_week_ago = timezone.now() - timedelta(days=7)


class HomeView(ListView):
    model = Post
    template_name = "News/home.html"
    queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
    context_object_name = "posts"


class PostListView(ListView):
    model = Post
    template_name = "News/body/post_list/post_list.html"
    queryset = Post.objects.filter(published_at__isnull=False).order_by("-published_at")
    context_object_name = "posts"
    paginate_by = paginate_by


class PostDetailView(DetailView):
    model = Post
    template_name = "News/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        obj.views_count += 1
        obj.save()
        context = super().get_context_data(**kwargs)
        context["comments"] = obj.comment_set.all().order_by('-created_at')[:10]
        context["previous_post"] = Post.objects.filter(
            id__lt=obj.id,
            status="active",
            published_at__isnull=False,
        ).first()
        context["next_post"] = Post.objects.filter(
            id__gt=obj.id,
            status="active",
            published_at__isnull=False,
        ).first()
        return context


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post_list.html"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")
    context_object_name = "posts"


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("draft-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("post-list")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("post-list")


class PostByCategory(ListView):
    model = Post
    template_name = "News/body/post_list/post_list.html"
    context_object_name = "posts"
    paginate_by = paginate_by

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="active", published_at__isnull=False, category=self.kwargs["cat_id"]
        )
        return queryset


class PostByTag(ListView):
    model = Post
    template_name = "News/body/post_list/post_list.html"
    context_object_name = "posts"
    paginate_by = paginate_by

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="active", published_at__isnull=False, tag=self.kwargs["tag_id"]
        )
        return queryset


class PostSearchView(View):
    template_name = "News/body/post_list/post_list.html"
    def get(self, request, *args, **kwargs):
        query = request.GET["query"]
        posts = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query))
            & Q(status="active")
            & Q(published_at__isnull=False)
        )
        return render(
            request,
            self.template_name,
            {
                "posts": posts,
            },
        )


class NewsLetterView(View):
    form_class = NewsLetterForm

    def post(self, request, *args, **kwargs):
        # ajax = XMLHttpRequest = submitting form without reloading pages
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "We have registered your email address",
                    },
                    status=200,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Something went wrong while submitting the form.",
                },
                status=400,
            )


class ContactView(View):
    template_name = "News/contact.html"
    form_class = ContactForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Successfully submitted your query. We will contact you soon."
            )
        else:
            messages.error(request, "Sorry, Something went wrong.")
        return render(request, self.template_name)


class AboutView(TemplateView):
    template_name = "News/about.html"


class CommentView(View):
    form_class = CommentForm

    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Successfully submitted your query. We will contact you soon."
            )
        else:
            messages.error(request, "Sorry, Something went wrong.")
        post_id = request.POST["post"]
        return redirect("post-detail", post_id)