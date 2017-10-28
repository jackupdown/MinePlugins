from django.db import models
from rbac.models import User as RbacUser


class UserInfo(models.Model):
    nickName = models.CharField(max_length=16)
    user = models.OneToOneField(RbacUser)

    def __str__(self):
        return self.nickName


class Order(models.Model):
    """
    报障单
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    detail = models.TextField(verbose_name='详细')
    createUser = models.ForeignKey(UserInfo, related_name='orderUser')
    createTime = models.DateTimeField(auto_now_add=True)
    statusChoices = (
        (1, '未处理'),
        (2, '处理中'),
        (3, '已处理')
    )
    status = models.IntegerField(choices=statusChoices, default=1)
    processor = models.ForeignKey(UserInfo, related_name='orderProcessor', null=True, blank=True)
    solution = models.TextField(null=True, blank=True)
    processTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title






















