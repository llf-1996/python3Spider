import requests
from fake_useragent import UserAgent
from scrapy.selector import Selector
import MySQLdb
conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="ip_pool",charset="utf8")
cursor = conn.cursor()
ua = UserAgent()

def crawl_ips():
    #爬取西刺的免费IP代理

    headers = {
        "User-Agent":ua.random
    }
    ip_list = []
    for i in range(1,2911):
        url = 'http://www.xicidaili.com/nn/{0}'.format(i)
        response = requests.get(url,headers = headers)
        # print(response.text)
        selector = Selector(text = response.text)
        all_trs = selector.css("#ip_list tr")
        for all_tr in all_trs[1:]:
            speed_str =all_tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0].strip())
            data = all_tr.css("td::text").extract()
            ip = data[0]
            port = data[1]
            ip_type = data[5]
            ip_list.append((ip,port,ip_type,speed))

        for ip_info in ip_list:
            cursor.execute("insert ignore into proxy_ip(ip,port,ip_type,speed) values(%s,%s,%s,%s)",ip_info)
            conn.commit()


class GetIP():
    def delete_ip(self,ip):
        delete_sql = """
        delete from proxy_ip where ip ='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self,ip,port):
        #判断IP是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip,port)
        try:
            headers = {
                "User-Agent":ua.random
            }
            proxy_dict = {
                "http":proxy_url
            }
            response = requests.get(http_url,headers=headers,proxies=proxy_dict)
            print(response.status_code)

        except Exception as e:
            print("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >=200 and code < 300:
                print("effective ip")
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        #从数据库中随机获取一个可用的IP
        random_sql = """
            select ip,port from proxy_ip
            where ip_type= "HTTP"
            order by RAND()
            LIMIT 1
        """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            judge = self.judge_ip(ip,port)
            if judge:
                return "http://{0}:{1}".format(ip,port)
            else:
                print('已删除...')
                return self.get_random_ip()


if __name__ == "__main__":
    # #爬取西刺ip代理
    # crawl_ips()

    #测试爬取的IP代理是否有效
    ip = GetIP()
    useful_ip = ip.get_random_ip()
    print(useful_ip)  #输出可用的IP代理

