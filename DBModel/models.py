from django.db import models

import os

# Create your models here.

class ReleaseAuthority(models.Model):
    token = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'release_authority'


def web_pic_path(instance, filename):
    ext = os.path.splitext(filename)[1];
    return os.path.join("release", "web", "img", f"{instance.name}{ext}");
class WebItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="名称")
    title = models.CharField(max_length=255, verbose_name="标题")
    thumbnail = models.ImageField(upload_to=web_pic_path, verbose_name="缩略图")
    description = models.TextField(verbose_name="描述")
    wtype = models.CharField(max_length=255, verbose_name="类型")
    url = models.CharField(max_length=255, verbose_name="网址")
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'url_item'


def game_pic_path(instance, filename):
    ext = os.path.splitext(filename)[1];
    return os.path.join("release", "game", "img", f"{instance.name}{ext}");
def game_file_path(instance, filename):
    ext = os.path.splitext(filename)[1];
    return os.path.join("release", "game", "file", f"{instance.name}{ext}");
class GameItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="名称")
    thumbnail = models.ImageField(upload_to=game_pic_path, blank=True, null=True, verbose_name="缩略图")
    description = models.TextField(verbose_name="描述")
    schedule = models.IntegerField(verbose_name="进度")
    file_path = models.FileField(upload_to = game_file_path, blank=True, null=True, verbose_name="游戏文件")
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'game_item'


class GameLog(models.Model):
    gid = models.ForeignKey('GameItem', models.DO_NOTHING, db_column='gid')
    title = models.CharField(max_length=255, verbose_name="标题")
    sub_title = models.CharField(max_length=255, verbose_name="子标题")
    content = models.TextField(verbose_name="内容")
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'game_log'
