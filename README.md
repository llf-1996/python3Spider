# python3Spider
关于python3爬虫的基本示例及项目。

## baseSpider非框架类爬虫
请求库urllib、requests；解析库beautifulsoup、lxml、pyquery；selenium的用法和应对反爬的代码示例。

## scrapySpider框架类爬虫
### 飞卢小说爬虫：
项目位置：https://github.com/llf-1996/python3Spider/tree/master/scrapySpider/%E9%A3%9E%E5%8D%A2%E5%B0%8F%E8%AF%B4/faloo
技术：scrapy框架：crawlspider模板、scrapy的xpath语法、文件存储；
start_url：https://b.faloo.com/f/531576.html
定义Rule规则匹配本小说的url进行小说的爬取，xpath提取数据,将爬取到的小说统一保存到feilu文件夹下以小说名为文件夹名以章节为文件名保存到本地。

### 笑话集爬虫：
项目位置：https://github.com/llf-1996/python3Spider/tree/master/scrapySpider/%E5%88%86%E5%B8%83%E5%BC%8F/Jokejiv1
技术：scrapy框架：rediscrawlspider模板、scrapy的xpath语法、redis、MySQL持久话数据（同步存取）
start_url：http://www.jokeji.cn/hot.htm
爬取字段：标题、链接、内容、发布时间、浏览数、爬取时间字段保存至MySQL，并使用Django分页展示数据和全文检索功能。
页面分析：
    初步分析此网站为静态页面
    在首页的搜索栏选择全部，点击搜索，进入搜索页的URL：http://www.jokeji.cn/search.asp，这应该是所有的笑话。
    通过rules爬取详情页url和分页的页数URL
详情页：
    关于笑话的详情页面中浏览量是js加载的，解决方法：使用requests请求script标签的src属性得到的内容中就有浏览量。
    关于页面中的内容使用xpath中的//text()得到list类型的内容，使用字符串的join()方法拼接。

### 招聘类网站：
**猎聘网爬虫**
技术：scrapy框架：crawlspider模板、scrapy的xpath语法、文件保存
项目位置：：https://github.com/llf-1996/python3Spider/tree/master/scrapySpider/liepinspiderv1

**拉钩网爬虫**
技术：scrapy框架：crawlspider模板、scrapy的xpath语法、mysql异步化保存；
项目位置：https://github.com/llf-1996/python3Spider/tree/master/scrapySpider/liepinspiderv1


### 技术文章类网站
**伯乐在线爬虫**
start_url：http://blog.jobbole.com/all-posts
技术：scrapy框架：crawlspider模板、scrapy的xpath语法、同步异步插入MySQL数据库、使用ImagesPipeline自动保存图片；
项目位置：https://github.com/llf-1996/python3Spider/tree/master/scrapySpider/four%20week/article

**简书网爬虫**
start_url：https://www.jianshu.com/c/20f7f4031550?order_by=added_at&page=1
技术：scrapy框架：crawlspider模板、scrapy的xpath语法、MongoDB数据库；
项目位置：https://github.com/llf-1996/python3Spider/tree/master/scrapySpider/jianshu-scrapy

