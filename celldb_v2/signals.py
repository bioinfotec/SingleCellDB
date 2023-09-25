from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import literature_info

@receiver(post_save, sender=literature_info)
def my_signal_handler(sender, instance, created, *args, **kwargs):
    # 处理信号
    print("信号已接收")
    if created:
        print("新建了一个文献信息")