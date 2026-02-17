#!/usr/bin/env python3
"""
OpenClaw AI Girlfriend - Test Script
测试脚本 - 验证基础功能
"""

import sys
import os

# 添加modules到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'openclaw-ai-girlfriend-by-clawra-main'))

from modules.brain import LLMBrain
from modules.onboarding import OnboardingWizard

def test_llm():
    """测试LLM功能"""
    print("\n=== 测试 LLM 功能 ===")
    brain = LLMBrain(use_real_api=False)  # 先使用模拟模式
    
    response = brain.generate_response(
        user_text="你好，你是谁？",
        personality_prompt="你是一个温柔体贴的虚拟女友"
    )
    print(f"用户: 你好，你是谁？")
    print(f"AI回复: {response}")
    return True

def test_onboarding():
    """测试引导流程"""
    print("\n=== 测试引导配置 ===")
    wizard = OnboardingWizard(profile_path="test_profile.json")
    
    # 检查是否存在profile
    if wizard.profile_exists():
        print("发现已有配置文件")
        profile = wizard.load_profile()
        print(f"配置内容: {profile}")
    else:
        print("没有找到配置文件，需要运行引导流程")
        print("(在实际使用中会交互式询问)")
    
    return True

def main():
    print("="*50)
    print("OpenClaw AI Girlfriend - 功能测试")
    print("="*50)
    
    try:
        # 测试各个模块
        test_llm()
        test_onboarding()
        
        print("\n" + "="*50)
        print("✅ 基础功能测试通过!")
        print("="*50)
        print("\n下一步:")
        print("1. 配置Ollama使用真实API")
        print("2. 安装Stable Diffusion WebUI")
        print("3. 配置Telegram/Discord Bot")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
