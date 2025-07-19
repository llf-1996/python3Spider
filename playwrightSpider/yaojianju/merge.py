import json
import pandas as pd
import os
from datetime import datetime

def load_task_process():
    """加载任务进度文件，获取所有需要合并的key"""
    with open("task_process.json", "r", encoding="utf-8") as f:
        task_process = json.load(f)
    return task_process

def merge_json_files():
    """合并所有JSON文件并输出为Excel"""
    # 加载任务进度文件
    task_process = load_task_process()
    
    # 用于存储所有数据的列表
    all_data = []
    
    # 遍历task_process中的所有key
    for key in task_process.keys():
        json_file = f'output/pharmaceutical_companies_{key}.json'
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)
                print(f"成功读取文件：{json_file}，数据条数：{len(data)}")
            except Exception as e:
                print(f"读取文件 {json_file} 时出错：{str(e)}")
    
    if not all_data:
        print("没有找到任何数据！")
        return
    
    # 转换为DataFrame
    df = pd.DataFrame(all_data)
    
    # 确保所有必要的列都存在
    required_columns = ['company_name', 'license_number']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"警告：数据中缺少以下字段：{missing_columns}")
        return
    
    # 删除重复数据
    df_no_duplicates = df.drop_duplicates(subset=['company_name', 'license_number'], keep='first')
    
    # 重命名列为中文
    df_no_duplicates = df_no_duplicates.rename(columns={
        'company_name': '企业名称',
        'license_number': '许可证号'
    })
    
    # 生成输出文件名（包含时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'output/药品经营企业信息_{timestamp}.xlsx'
    
    # 保存为Excel文件，只保存这两个字段
    df_no_duplicates[['企业名称', '许可证号']].to_excel(
        output_file, 
        index=False, 
        engine='openpyxl'
    )
    
    print(f"\n合并完成！")
    print(f"原始数据总条数：{len(all_data)}")
    print(f"去重后数据条数：{len(df_no_duplicates)}")
    print(f"输出文件：{output_file}")
    print("\nExcel文件包含以下字段：")
    print("1. 企业名称")
    print("2. 许可证号")

if __name__ == "__main__":
    merge_json_files()