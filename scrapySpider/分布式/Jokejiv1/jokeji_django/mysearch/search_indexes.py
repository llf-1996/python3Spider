"""
__title__ = ''
__author__ = 'llf'
__mtime__ = '...'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from haystack import indexes
from jokeji.models import Jokeji


class JokejiIndex(indexes.SearchIndex, indexes.Indexable):
    # 给笑话类添加索引
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Jokeji

    def index_queryset(self, using=None):
        return self.get_model().objects.all()



