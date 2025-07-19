# 药品经营企业信息采集

这是一个使用Playwright开发的爬虫项目，用于采集国家药品监督管理局网站的药品经营企业信息。

## 功能特点

- 自动采集药品经营企业信息
- 支持多省份数据采集
- 自动处理反爬措施
- 数据自动去重和合并
- 支持导出为Excel格式

## 环境要求

- Python 3.11+
- 依赖包：
  - playwright==1.41.2
  - pandas==2.2.0
  - openpyxl==3.1.2

## 安装步骤

1. 克隆项目到本地

2. 安装依赖（使用阿里云镜像加速）：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

3. 安装Playwright浏览器：
```bash
playwright install chromium
```

## 使用方法

1. 运行爬虫程序：
```bash
python main.py
```
- 程序会自动遍历所有省份
- 采集的数据会保存在output目录下的JSON文件中
- 每个省份的数据会单独保存

2. 合并数据（可选）：
```bash
python merge.py
```
- 将所有JSON文件合并为一个Excel文件
- 自动去除重复数据
- 输出文件包含企业名称和许可证号
- 输出文件名格式：pharmaceutical_companies_merged_时间戳.xlsx

## 数据存储

- 原始数据：保存在output目录下的JSON文件中
- 合并后数据：保存在output目录下的Excel文件中
- 任务进度：保存在task_process.json中

## 注意事项

1. 运行环境：
   - 确保使用Python 3.11或更高版本
   - 确保安装了所有依赖包
   - 确保已安装Playwright浏览器

2. 数据采集：
   - 程序会自动处理网络延迟和错误
   - 支持断点续采
   - 自动保存采集进度

3. 反爬虫：
   - 已实现基本的反爬虫措施
   - 包含随机延迟
   - 模拟真实浏览器行为

## 文件说明

- `main.py`: 主程序文件，实现爬虫功能
- `merge.py`: 数据合并程序，用于合并JSON文件并输出Excel
- `requirements.txt`: 依赖包列表
- `province.json`: 省份配置文件
- `task_process.json`: 任务进度记录文件
- `output/`: 输出目录，存放采集的数据文件 