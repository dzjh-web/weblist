from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.db import models

import os

# Create your models here.

def carouse_img_path(instance, filename):
    ext = os.path.splitext(filename)[1];
    return os.path.join("release", "carouse", "img", f"{instance.name}{ext}");
class Carouse(models.Model):
    name = models.CharField(max_length=255, verbose_name="名称")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="标题")
    url = models.CharField(max_length=255, verbose_name="链接")
    img = models.ImageField(upload_to=carouse_img_path, blank=True, null=True, verbose_name="图片")
    alt = models.CharField(max_length=255, blank=True, null=True, verbose_name="图片描述")
    wtype = models.IntegerField()
    time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'carouse'


def game_pic_path(instance, filename):
    ext = os.path.splitext(filename)[1];
    return os.path.join("release", "game", "img", f"{instance.name}{ext}");
def game_file_path(instance, filename):
    ext = os.path.splitext(filename)[1];
    return os.path.join("release", "game", "file", f"{instance.name}{ext}");
class GameItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="名称")
    category = models.CharField(max_length=255, verbose_name="类型")
    thumbnail = models.ImageField(upload_to=game_pic_path, verbose_name="缩略图")
    description = models.CharField(max_length=255, verbose_name="简述")
    cid = models.ForeignKey('WebContent', models.DO_NOTHING, db_column='cid')
    schedule = models.IntegerField(verbose_name="进度")
    file_path = models.FileField(upload_to = game_file_path, blank=True, null=True, verbose_name="游戏文件")
    time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'game_item'

# 删除文件
@receiver(pre_delete, sender=GameItem)
def game_item_delete(sender, instance, **kwargs):
    instance.thumbnail.delete(False)
    instance.cid.delete(False)


class GameLog(models.Model):
    gid = models.ForeignKey('GameItem', models.DO_NOTHING, db_column='gid')
    title = models.CharField(max_length=255, verbose_name="标题")
    sub_title = models.CharField(max_length=255, verbose_name="子标题")
    sketch = models.CharField(max_length=255)
    cid = models.ForeignKey('WebContent', models.DO_NOTHING, db_column='cid')
    time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'game_log'

# 删除文件
@receiver(pre_delete, sender=GameLog)
def game_log_delete(sender, instance, **kwargs):
    instance.cid.delete(False)


class ResumeToken(models.Model):
    token = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    expires = models.IntegerField(verbose_name="有效期（天）")
    create_at = models.DateTimeField()
    active_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'resume_token'


class WebContent(models.Model):
    content = RichTextUploadingField(verbose_name="内容")

    class Meta:
        managed = False
        db_table = 'web_content'


def web_pic_path(instance, filename):
    ext = os.path.splitext(filename)[1];
    return os.path.join("release", "web", "img", f"{instance.name}{ext}");
class WebItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="名称")
    title = models.CharField(max_length=255, verbose_name="标题")
    thumbnail = models.ImageField(upload_to=web_pic_path, verbose_name="缩略图")
    description = models.CharField(max_length=255, verbose_name="简述")
    url = models.CharField(max_length=255, verbose_name="网址")
    cid = models.ForeignKey('WebContent', models.DO_NOTHING, db_column='cid')
    wtype = models.IntegerField()
    state = models.IntegerField()
    time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'web_item'

# 删除文件
@receiver(pre_delete, sender=WebItem)
def web_item_delete(sender, instance, **kwargs):
    instance.thumbnail.delete(False)
    instance.cid.delete(False)