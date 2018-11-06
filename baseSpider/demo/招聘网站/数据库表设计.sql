
# 招聘信息爬虫表结构
CREATE TABLE jobinfo(
id INT AUTO_INCREMENT PRIMARY KEY COMMENT '数据编号',
job_name VARCHAR(200) COMMENT '招聘职位',
job_url VARCHAR(200) COMMENT '招聘职位链接',
company_name VARCHAR(200) COMMENT '公司名',
company_url VARCHAR(200) COMMENT '公司链接',
work_addr VARCHAR(200) COMMENT '工作地点',
money VARCHAR(200) COMMENT '薪资',
publish_time VARCHAR(200) COMMENT '职位发布时间',
crawl_time DATETIME COMMENT '爬取时间',
data_from VARCHAR(200) COMMENT '数据来源'
)DEFAULT CHARSET 'utf8';





