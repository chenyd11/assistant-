#!/usr/bin/env python3
"""
发布到 抖音 - 主账号
生成时间: 2026-02-15T21:22:28.177825
"""

CONTENT = {
  "title": "进厂打工前必问的9个问题",
  "body": "进厂打工，这9个问题不问清楚，等着被坑！\n第一，厂名叫什么？不敢说的直接拉黑。\n第二，地址在哪？写字楼面试、地铁口集合的都是中介套路。\n第三，工资怎么算？纯工价还是补差价？合同逐字看，别掉陷阱。\n第四，有哪些费用？押金、体检费？正规厂不收这些。\n第五，啥时候发工资？离职后超过7天才结的，快跑。\n第六，吃住真包吗？问清楚是纯包还是餐补，几人间。\n第七，给工资条吗？不敢给的绝对有猫腻。\n第八，工期多久？做不到怎么算？提前几天离职？",
  "tags": [
    "#进厂打工",
    "#避坑指南",
    "#求职",
    "#干货"
  ]
}

def publish():
    print("=" * 60)
    print("📱 发布到: 抖音")
    print("👤 账号: 主账号")
    print("=" * 60)
    print()
    print("标题:")
    print(f"  {CONTENT['title']}")
    print()
    print("内容:")
    print(f"  {CONTENT['body'][:200]}...")
    print()
    if CONTENT.get('tags'):
        print("标签:")
        print(f"  {', '.join(CONTENT['tags'])}")
    print()
    
    # TODO: 实现浏览器自动化
    # 1. 打开 https://creator.douyin.com
    # 2. 登录账号
    # 3. 创建新内容
    # 4. 填充标题、正文、标签
    # 5. 发布
    
    print("⚠️  请手动完成以下步骤:")
    print("  1. 打开 https://creator.douyin.com")
    print("  2. 登录账号: 主账号")
    print("  3. 创建新内容")
    print("  4. 复制以下内容:")
    print()
    print("-" * 40)
    print(CONTENT['title'])
    print("-" * 40)
    print(CONTENT['body'])
    print("-" * 40)
    if CONTENT.get('tags'):
        print("标签: " + " ".join(CONTENT['tags']))
    print("-" * 40)
    print()
    input("发布完成后按回车键继续...")

if __name__ == "__main__":
    publish()
