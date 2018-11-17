from django.db import models

# Create your models here.


class Jokeji(models.Model):
    '''
    商品类型类
    '''
    id = models.AutoField(primary_key=True, verbose_name='数据编号')
    title = models.CharField(max_length=255, verbose_name="标题")
    url = models.CharField(max_length=255, verbose_name="链接")
    content = models.TextField(verbose_name="内容")
    publish_time = models.CharField(max_length=255, verbose_name="发布时间")
    view_num = models.TextField(verbose_name="浏览数")
    crawled_time = models.DateTimeField(verbose_name="爬取时间")
    data_from = models.CharField(max_length=255, verbose_name="数据来源")

    class Meta:
        # 设置表名，如果不设置表名为模块名_类名
        db_table = 'jokeji'
        # 对all、filter查询结果排序
        ordering = ['-publish_time']
