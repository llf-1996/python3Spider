# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

'''
from scrapy.item import Item,Field
class ArticleItem(Item):
    title   =   Field()
    create_date=Field()
    praise_nums=Field()
    fav_nums=Field()
    comments_nums=Field()
    content=Field()
    tag = Field()

'''
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
from scrapy.loader import ItemLoader
import re
from article.settings import SQL_DATE_FORMAT,SQL_DATETIME_FORMAT

def add_jobbole(value):
    return value + "-boby"


def date_convert(value):
    value = value.replace("·","").strip()
    try:
        create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*",value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def remove_comment_tags(value):
    #去掉tags中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title=scrapy.Field(
        #input_processor = MapCompose(add_jobbole)
        input_processor = MapCompose(lambda x:x + "-jobbole",add_jobbole)
    )
    create_date=scrapy.Field(
        input_processor=MapCompose(date_convert),
        output_processor = TakeFirst()
    )
    praise_nums=scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    fav_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comments_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content=scrapy.Field()
    tag = scrapy.Field(
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join("-")
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()

