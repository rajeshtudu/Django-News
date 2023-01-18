from django.db import models

# This is timestamp model
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStamp):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name[:100]


class Tag(TimeStamp):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name[:100]


class Post(TimeStamp):  # Pascal case
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    views_count = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="active")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tag = models.ManyToManyField(Tag)
    published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.title[:100]


class NewsLetter(TimeStamp):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Contact(TimeStamp):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.subject


class Comment(TimeStamp):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    name = models.CharField(max_length=200)
    email = models.EmailField()


#################### 1 - 1 relationship => OneToOneField
# 1 user can have only 1 profile => 1
# 1 profile is associated to only 1 user => 1

#################### 1 - M relationship => ForeignKey => in M
# 1 user can post M post => M
# 1 post is associate to only 1 user => 1


##################### M - M relationship
# 1 post can have M tag => M
# 1 tag can have M post => M


# 1 teacher teaches M student => M
# 1 student learn from M teacher = M