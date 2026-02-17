#!/usr/bin/env python3
"""
飞书Bitable视频库自动同步脚本
"""

import json
import requests
import os

# 从环境变量获取token（需要配置）
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")

# Bitable信息
APP_TOKEN = "V87Cb06erar7kGsTFm0cR0JZnof"
BASE_URL = "https://open.feishu.cn/open-apis/bitable/v1"

def get_tenant_token():
    """获取tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    resp = requests.post(url, headers=headers, json=data)
    return resp.json().get("tenant_access_token")

def list_tables(token):
    """列出所有表格"""
    url = f"{BASE_URL}/apps/{APP_TOKEN}/tables"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    return resp.json()

def list_fields(token, table_id):
    """列出表格字段"""
    url = f"{BASE_URL}/apps/{APP_TOKEN}/tables/{table_id}/fields"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    return resp.json()

def add_record(token, table_id, fields):
    """添加记录"""
    url = f"{BASE_URL}/apps/{APP_TOKEN}/tables/{table_id}/records"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {"fields": fields}
    resp = requests.post(url, headers=headers, json=data)
    return resp.json()

if __name__ == "__main__":
    print("视频库Bitable同步工具")
    print("=" * 50)
    print()
    
    # 检查配置
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        print("⚠️  请先配置飞书应用凭证:")
        print("   export FEISHU_APP_ID=your_app_id")
        print("   export FEISHU_APP_SECRET=your_app_secret")
        print()
        print("获取方式：")
        print("1. 打开 https://open.feishu.cn/app")
        print("2. 创建企业自建应用")
        print("3. 获取 App ID 和 App Secret")
        print("4. 申请 Bitable 权限")
        exit(1)
    
    # 获取token
    token = get_tenant_token()
    print(f"✅ 已获取访问令牌")
    
    # 列出表格
    tables = list_tables(token)
    print(f"\n📊 表格列表:")
    print(json.dumps(tables, indent=2, ensure_ascii=False))
