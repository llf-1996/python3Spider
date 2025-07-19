import asyncio
from playwright.async_api import async_playwright
import time
import json
from datetime import datetime
import re
import traceback
import os
import random

from db import init_database, save_to_database

# 确保output目录存在
os.makedirs('output', exist_ok=True)

async def load_province():
    with open("province.json", "r", encoding="utf-8") as f:
        province = json.load(f)
    return province

async def load_task_process():
    with open("task_process.json", "r", encoding="utf-8") as f:
        task_process = json.load(f)
    return task_process

async def save_task_process(task_process):
    with open("task_process.json", "w", encoding="utf-8") as f:
        json.dump(task_process, f, ensure_ascii=False, indent=2)

async def get_current_task_process(task_process, key):
    if key not in task_process:
        task_process[key] = {
            "status": "wait",
            "count": 0,
            "current_page": 1,
            "total_page": 1
        }
    return task_process[key]

# 添加随机延迟函数
async def random_delay(page, min_seconds=1, max_seconds=3):
    delay = min_seconds + (max_seconds - min_seconds) * random.random()
    await page.wait_for_timeout(int(delay * 1000))

async def get_data(page, search_key, task_process):
    all_companies = []
    try:
        items_per_page = 20  # 每页显示20条
        # 检查并切换每页显示条数为20条
        print("检查每页显示条数...")
        page_input_selector = '#home > div.container > div.page.pc-max > div > div > span.el-pagination__sizes > div > div.el-input.el-input--mini.el-input--suffix > input'
        # 获取当前每页显示条数
        current_size = await page.evaluate(f'document.querySelector("{page_input_selector}").value')
        print(f"当前每页显示条数：{current_size}")
        # 如果不是20条/页，则进行切换
        if current_size != f"{items_per_page}条/页":
            print("正在切换为20条/页...")
            page_size_selector = '.el-pagination__sizes .el-input__inner'
            await page.wait_for_selector(page_size_selector)
            await page.click(page_size_selector)
            await random_delay(page, 1, 2)
            # 选择20条/页选项
            page_size_20_option = 'body > div.el-select-dropdown.el-popper > div.el-scrollbar > div.el-select-dropdown__wrap.el-scrollbar__wrap > ul > li:nth-child(2)'
            await page.wait_for_selector(page_size_20_option)
            await page.click(page_size_20_option)
            await random_delay(page, 2, 3)
        else:
            print("已经是20条/页，无需切换")
        # 等待并填写搜索框
        search_selector = 'div.sousuo.putongsousuo > div > input'
        await page.wait_for_selector(search_selector)
        await page.fill(search_selector, search_key)
        await page.wait_for_timeout(1000)
        
        # 点击搜索按钮
        search_button = 'div.sousuo.putongsousuo > div > div > button'
        await page.wait_for_selector(search_button)
        await page.click(search_button)
        print("已发起搜索请求...")
        
        await random_delay(page, 3, 6)  # 随机延迟3-6秒
        # 等待搜索结果加载
        await page.wait_for_selector('#home > div.container > div.search-result-table', state='visible')
        await random_delay(page, 3, 6)  # 随机延迟3-6秒

        # 获取总页数
        total_selector = '#home > div.container > div.page.pc-max > div > div > span.el-pagination__total'
        await page.wait_for_selector(total_selector)
        total_text = await page.text_content(total_selector)
        if not total_text:
            print("未能获取到分页信息文本")
            return False
        total_text = total_text.strip()
        
        # 使用正则表达式提取数字，允许空格
        match = re.search(r'共\s*(\d+)\s*条', total_text)
        if not match:
            print("未找到总条数信息", total_text)
            return False
            
        total_items = int(match.group(1))
        total_pages = (total_items + items_per_page - 1) // items_per_page  # 向上取整
        if total_pages == 0:
            print("无数据跳过")
            return True
        if total_items > 10000:
            # 最多查看1万条
            print(f"超过1万条数据，开始拆分采集")
            successed = True
            for i in range(10):
                is_ok = await get_data(page, f"{search_key}{i}", task_process)
                if not is_ok:
                    successed = False
            return successed

        print(f"总条数：{total_items}，每页{items_per_page}条，共{total_pages}页")
        current_task_process = await get_current_task_process(task_process, search_key)
        if current_task_process["status"] == "success":
            print(f"采集{search_key}已完成")
            return True

        # 从search_key中提取省份信息（假设search_key的第一个字符是省份）
        province = search_key[0]  # 例如：豫、京、沪等
        print(f"采集{search_key}...")
        current_task_process["total_page"] = total_pages
        current_task_process["count"] = total_items
        current_task_process["status"] = "run"
        
        while current_task_process["current_page"] <= current_task_process["total_page"]:
            print(f"正在采集第 {current_task_process['current_page']} 页")
            # 使用输入框跳转到下一页
            page_input_selector = '#home > div.container > div.page.pc-max > div > div > span.el-pagination__jump > div > input'
            await page.wait_for_selector(page_input_selector)
            # 清空输入框并输入新的页码
            await page.click(page_input_selector)
            await page.keyboard.press('Control+A')
            await page.keyboard.press('Backspace')
            await page.type(page_input_selector, str(current_task_process["current_page"]))
            await page.keyboard.press('Enter')
            # 等待企业列表加载
            table_selector = '#home > div.container > div.search-result-table > div > div > div.el-table__body-wrapper.is-scrolling-none > table'
            await page.wait_for_selector(table_selector)
            await random_delay(page, 3, 6)  # 随机延迟3-6秒
            # 获取当前页的企业信息
            companies = await page.evaluate('''
                (selector) => {
                    const table = document.querySelector(selector);
                    if (!table) return [];
                    
                    const rows = table.querySelectorAll('tr');
                    return Array.from(rows).map(row => {
                        const indexCell = row.querySelector('.el-table_1_column_1 .cell div');
                        const nameCell = row.querySelector('.el-table_1_column_2 p, .el-table_1_column_2 .name-wrapper');
                        const licenseCell = row.querySelector('.el-table_1_column_3 p');
                        
                        // 获取企业名称，处理可能的省略号情况
                        let name = nameCell ? nameCell.textContent.trim() : '';
                        if (name.endsWith('...')) {
                            // 如果有完整名称，则从tooltip中获取
                            const tooltip = row.querySelector('.el-popover p');
                            if (tooltip) {
                                name = tooltip.textContent.trim();
                            }
                        }
                        
                        return {
                            index: indexCell ? indexCell.textContent.trim() : '',
                            company_name: name,
                            license_number: licenseCell ? licenseCell.textContent.trim() : ''
                        };
                    });
                }
            ''', table_selector)
            
            for company in companies:
                if company in all_companies:
                    continue
                all_companies.append(company)
                
            if (
                current_task_process["current_page"] >= current_task_process["total_page"]
                or len(companies) == 0
            ):
                current_task_process["status"] = "success"
                break
            current_task_process["current_page"] += 1
        return True
    except Exception as e:
        print(f"信息提取失败：{e}")
        traceback.print_exc()
        return False
    finally:
        # 保存到数据库
        if len(all_companies) > 0:
            await save_to_database(all_companies, province)
            print(f"已保存{len(all_companies)}条数据到数据库")
        # 保存任务进度
        print("保存任务进度...")
        await save_task_process(task_process)

async def save_province(provinces):
    """
    保存省份状态到province.json文件
    
    Args:
        provinces (dict): 省份状态字典，key为省份简称，value为状态（0或1）
    """
    with open("province.json", "w", encoding="utf-8") as f:
        json.dump(provinces, f, ensure_ascii=False, indent=2)

async def main():
    # 初始化数据库
    init_database()
    
    task_process = await load_task_process()
    async with async_playwright() as p:
        # 设置浏览器参数
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器界面
            args=[
                '--disable-blink-features=AutomationControlled',  # 禁用自动化控制检测
                '--disable-infobars',  # 禁用信息栏
                '--start-maximized',  # 最大化窗口
                '--disable-blink-features',  # 禁用一些特征
                '--disable-automation',  # 禁用自动化
                '--disable-dev-shm-usage',  # 禁用/dev/shm使用
                '--no-sandbox',  # 禁用沙箱
                '--lang=zh-CN',  # 设置语言
                '--disable-gpu',  # 禁用GPU加速
                '--disable-setuid-sandbox',  # 禁用setuid沙箱
                '--disable-webgl',  # 禁用WebGL
                '--disable-webgl2',  # 禁用WebGL2
                '--disable-notifications',  # 禁用通知
                '--ignore-certificate-errors',  # 忽略证书错误
            ]
        )
        
        # 创建上下文
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},  # 设置视窗大小
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',  # 设置UA
            locale='zh-CN',  # 设置地区
            timezone_id='Asia/Shanghai',  # 设置时区
        )

        # 设置cookie
        await context.add_cookies([
            {
                'name': 'STEP_TIPS_INDEX',
                'value': 'true',
                'domain': 'www.nmpa.gov.cn',
                'path': '/'
            },
            {
                'name': 'STEP_TIPS_RESULT',
                'value': 'true',
                'domain': 'www.nmpa.gov.cn',
                'path': '/'
            },
        ])
        
        # 创建新页面
        page = await context.new_page()
        
        # 设置页面超时时间
        page.set_default_timeout(60000)  # 60秒

        print("正在进入首页...")
        await page.goto('https://www.nmpa.gov.cn/', wait_until='networkidle')
        await random_delay(page)  # 使用随机延迟

        # 设置localStorage
        await page.evaluate('''
            () => {
                const data = {
                    detailFeild: [{"width":"","alias":"f0","desc":"企业名称"},{"subTitle":"Y","width":"","alias":"f1","desc":"许可证编号"},{"width":"","alias":"f2","desc":"注册地址"},{"width":"","alias":"f3","desc":"法定代表人"},{"width":"","alias":"f4","desc":"企业负责人"},{"width":"","alias":"f5","desc":"质量负责人"},{"width":"","alias":"f6","desc":"经营方式"},{"width":"","alias":"f7","desc":"仓库地址"},{"width":"","alias":"f8","desc":"经营地址"},{"width":"","alias":"f9","desc":"经营范围"},{"width":"","alias":"f10","desc":"发证机关"},{"width":"","alias":"f11","desc":"有效期至"},{"width":"","alias":"f12","desc":"发证日期"},{"width":"","alias":"f13","desc":"许可证状态"},{"width":"","alias":"f14","desc":"NMPA_DK"}],
                    itemId: "ff808081817f00dc01818e18c7c80bde",
                    itemIdArray: ["ff808081817f00dc01818e18c7c80bde"],
                    itemName: "药品经营企业",
                    paraCode: "item_2",
                    searchkey: "豫B",
                    selectValue: [["item_2","ff808081817f00dc01818e18c7c80bde"]]
                };
                
                // 将数据写入localStorage，只对非字符串类型进行JSON序列化
                for (const [key, value] of Object.entries(data)) {
                    if (typeof value === 'string') {
                        localStorage.setItem(key, value);
                    } else {
                        localStorage.setItem(key, JSON.stringify(value));
                    }
                }
            }
        ''')
        await page.wait_for_timeout(1000)  # 等待localStorage设置完成

        print("正在进入数据查询页面...")
        await page.goto('https://www.nmpa.gov.cn/datasearch/search-result.html', wait_until='networkidle')
        await page.wait_for_timeout(2000)  # 等待2秒
        
        provinces = await load_province()
        try:
            # 获取省份状态
            for province, status in provinces.items():
                print(f"开始采集{province}...")
                successed = True
                if status == 1:
                    print(f"已采集完成，跳过...")
                    continue
                for type_key in ["A", "B", "C", "D"]:
                    for type_key2 in ["A", "B"]:
                        search_key = f"{province}{type_key}{type_key2}"
                        is_ok = await get_data(page, search_key, task_process)
                        if not is_ok:
                            successed = False
                if successed:
                    provinces[province] = 1
                    print(f"采集完成，更新状态...")
                    await save_province(provinces)
        except Exception as e:
            print(f"发生错误: {str(e)}")
            traceback.print_exc()
            error_screenshot = f'output/error_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            try:
                await page.screenshot(path=error_screenshot)
                print(f"错误截图已保存：{error_screenshot}")
            except:
                print("保存错误截图失败")
        finally:
            try:
                await context.close()
                await browser.close()
            except:
                pass
            print("浏览器已关闭。")

if __name__ == "__main__":
    asyncio.run(main())
