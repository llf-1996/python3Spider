数据库：
# 库
CREATE DATABASE IF NOT EXISTS pythonspider DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
# cookies池表
CREATE TABLE tbcookies(
id INT AUTO_INCREMENT PRIMARY KEY COMMENT '编号',
username VARCHAR(200) COMMENT '用户名',
passwd VARCHAR(200) COMMENT '密码',
cookies TEXT COMMENT 'cookies信息',
home_url VARCHAR(200) COMMENT '首页url'
)DEFAULT CHARSET 'utf8';


selenium登录后获取的cookie格式如下:
[
{'domain': '.weibo.com', 'httpOnly': False, 'name': 'login_sid_t', 'path': '/', 'secure': False, 'value': '7d5efdc418037a000cbd4bf2a56bd645'},
 {'domain': '.weibo.com', 'httpOnly': False, 'name': 'cross_origin_proto', 'path': '/', 'secure': False, 'value': 'SSL'},
 {'domain': 'weibo.com', 'expiry': 1543305114, 'httpOnly': False, 'name': 'WBStorage', 'path': '/', 'secure': False, 'value': 'f44cc46b96043278|undefined'},
 {'domain': 'weibo.com', 'httpOnly': False, 'name': 'Ugrow-G0', 'path': '/', 'secure': False, 'value': 'e66b2e50a7e7f417f6cc12eec600f517'},
 {'domain': '.weibo.com', 'expiry': 1574408521, 'httpOnly': False, 'name': 'ULV', 'path': '/', 'secure': False, 'value': '1543304521121:1:1:1:4417214637059.426.1543304521113:'},
 {'domain': 'weibo.com', 'httpOnly': False, 'name': 'YF-V5-G0', 'path': '/', 'secure': False, 'value': '*************'},
 {'domain': '.weibo.com', 'httpOnly': False, 'name': '_s_tentry', 'path': '/', 'secure': False, 'value': '-'},
 {'domain': '.weibo.com', 'expiry': 1858664521, 'httpOnly': False, 'name': 'SINAGLOBAL', 'path': '/', 'secure': False, 'value': '4417214637059.426.1543304521113'},
 {'domain': '.weibo.com', 'httpOnly': False, 'name': 'Apache', 'path': '/', 'secure': False, 'value': '4417214637059.426.1543304521113'},
 {'domain': '.weibo.com', 'expiry': 1574840536.04607, 'httpOnly': False, 'name': 'SUHB', 'path': '/', 'secure': False, 'value': '0oUou1Pw4dSitq'},
 {'domain': '.weibo.com', 'expiry': 1574840536.045939, 'httpOnly': False, 'name': 'SUBP', 'path': '/', 'secure': False, 'value': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5i18Aw7NyeAg6CaaNECPyx5JpX5K2hUgL.Foqceh50Sh27eK52dJLoIEXLxK-LBK-L1hMLxK-LBo5L12qLxK.L1h-LBoMLxK-LB.-LB--LxK-L12BL1-2t'},
 {'domain': '.weibo.com', 'expiry': 1574840533.046519, 'httpOnly': False, 'name': 'ALF', 'path': '/', 'secure': False, 'value': '1574840532'},
 {'domain': '.weibo.com', 'httpOnly': False, 'name': 'SSOLoginState', 'path': '/', 'secure': False, 'value': '*******'},
 {'domain': '.weibo.com', 'expiry': 1858664536.0457, 'httpOnly': True, 'name': 'SCF', 'path': '/', 'secure': False, 'value': 'Am9Dq1k70xs0VtQ3Sk8u6Cm_jgQQ8J23OPbriAzyaf_vqjdgm-qWzmLFf_NF6jGY_BzEQqNlOPI4v-Qi3h60lSo.'},
 {'domain': '.weibo.com', 'httpOnly': True, 'name': 'SUB', 'path': '/', 'secure': False, 'value': '_2A252-IUGDeRhGeBI61IS9C_MyjyIHXVVj_HOrDV8PUNbmtAKLW_hkW9NRqLCtzbaOizj3Mf56XboJBxAY5ET-8cu'},
 {'domain': '.weibo.com', 'expiry': 1544168536, 'httpOnly': False, 'name': 'un', 'path': '/', 'secure': False, 'value': '*******'},
 {'domain': '.weibo.com', 'expiry': 1543909337.438868, 'httpOnly': False, 'name': 'wvr', 'path': '/', 'secure': False, 'value': '6'}]
因此需要提前name和value字段值得到cookie。
