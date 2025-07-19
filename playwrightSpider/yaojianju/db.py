import sqlite3
import aiosqlite
import os
from datetime import datetime, timezone, timedelta

# 确保output目录存在
os.makedirs('output', exist_ok=True)

# 数据库文件路径
DB_FILE = 'output/pharmaceutical_companies.sqlite'

def init_database():
    """初始化数据库，创建表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 设置时区为北京时间（UTC+8）
    cursor.execute("PRAGMA timezone = '+08:00'")
    
    # 创建企业信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        license_number TEXT NOT NULL,
        province TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT (datetime('now', '+8 hours')),
        UNIQUE(company_name, license_number)
    )
    ''')
    conn.commit()
    conn.close()

def get_beijing_time():
    """获取北京时间"""
    beijing_tz = timezone(timedelta(hours=8))
    return datetime.now(beijing_tz)

async def save_to_database(companies, province):
    """
    保存企业信息到数据库
    
    Args:
        companies (list): 企业信息列表，每个企业是一个字典，包含company_name和license_number
        province (str): 省份代码，如"豫"、"京"等
    """
    beijing_time = get_beijing_time().strftime('%Y-%m-%d %H:%M:%S')
    async with aiosqlite.connect(DB_FILE) as db:
        # 保存企业信息
        for company in companies:
            try:
                await db.execute(
                    'INSERT OR IGNORE INTO companies (company_name, license_number, province, created_at) VALUES (?, ?, ?, ?)',
                    (company['company_name'], company['license_number'], province, beijing_time)
                )
            except Exception as e:
                print(f"保存企业信息失败：{str(e)}")
                continue
        await db.commit()

async def get_province_status():
    """获取省份状态"""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT province, status FROM province_status') as cursor:
            return {row[0]: row[1] async for row in cursor}

async def get_company_count():
    """获取数据库中的企业总数"""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT COUNT(*) FROM companies') as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def get_province_statistics():
    """获取各省份的数据统计"""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute('SELECT province, COUNT(*) as count FROM companies GROUP BY province') as cursor:
            return {row[0]: row[1] async for row in cursor}

async def get_latest_companies(limit=10):
    """获取最新添加的企业信息"""
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute(
            'SELECT company_name, license_number, province, created_at FROM companies ORDER BY created_at DESC LIMIT ?',
            (limit,)
        ) as cursor:
            return [dict(zip(['company_name', 'license_number', 'province', 'created_at'], row)) async for row in cursor] 