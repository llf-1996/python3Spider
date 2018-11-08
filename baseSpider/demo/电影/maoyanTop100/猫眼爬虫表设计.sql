# 猫眼电影top100爬虫
DROP DATABASE maoyantop100 IF EXISTS;

CREATE DATABASE pythonSpider DEFAULT CHARSET 'utf8';

CREATE TABLE maoyantop100(
the_index INT NOT NULL PRIMARY KEY COMMENT '电影排名',
image_url VARCHAR(255) COMMENT '电影图片链接',
title VARCHAR(200) COMMENT '电影名字',
actor VARCHAR(200) COMMENT '主演',
the_time VARCHAR(200) COMMENT '上映时间',
score VARCHAR(20) COMMENT '评分'
)DEFAULT CHARSET 'utf8';

DROP TABLE maoyantop100;

