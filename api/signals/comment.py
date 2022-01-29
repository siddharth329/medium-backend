from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from ..models import Comment


@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, **kwargs):
    instance.post.comment_count += 1
    instance.post.save()


@receiver(post_delete, sender=Comment)
def comment_post_delete(sender, instance, **kwargs):
    instance.post.comment_count -= 1
    instance.post.save()
