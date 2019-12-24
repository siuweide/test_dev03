from django.db import models

# Create your models here.

class variable(models.Model):
    """
    用户自定义变量表
    """
    key = models.CharField("名称", max_length=100, blank=False)
    value = models.TextField("值", max_length=500, blank=False)
    describe = models.TextField("描述", default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.key
