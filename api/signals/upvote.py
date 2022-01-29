from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from ..models import Upvote


@receiver(post_save, sender=Upvote)
def upvote_post_save(sender, instance, **kwargs):
    instance.post.upvote_count += 1
    instance.post.save()


@receiver(post_delete, sender=Upvote)
def upvote_post_delete(sender, instance, **kwargs):
    instance.post.upvote_count -= 1
    instance.post.save()