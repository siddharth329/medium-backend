from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.utils import timezone
from ..utils import generate_random_string
from ..models import Post
import readtime


@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, **kwargs):
    if instance.id is None:
        instance.slug = slugify(instance.title) + '-' + generate_random_string(8)
        instance.read_time = str(readtime.of_text(instance.content)).split(' ')[0]
        if instance.published:
            instance.published_at = timezone.now()

    else:
        previous = Post.objects.get(pk=instance.id)
        print(previous)

        if not previous.published and instance.published:
            instance.published_at = timezone.now()

        if previous.content != instance.content:
            instance.read_time = str(readtime.of_text(instance.content)).split(' ')[0]
