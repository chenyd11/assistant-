# SD WebUI 本地部署 - 回家操作指南

## 📥 必须下载的文件

### 1. 基础模型（必需）
**文件**: `v1-5-pruned-emaonly.safetensors`  
**大小**: ~4GB  
**下载地址**:
- 推荐: https://hf-mirror.com/runwayml/stable-diffusion-v1-5
- 备用: https://civitai.com/models/4201/realistic-vision-v60-b1

**放置位置**:
```
/Users/chenyd11/.openclaw/workspace/stable-diffusion-webui/models/Stable-diffusion/
```

---

### 2. 你的 LoRA（从 RunningHub）
**文件**: `my_lora_girl.safetensors`  
**大小**: ~50MB  
**下载步骤**:
1. 访问 https://www.runninghub.cn
2. 登录 → 工作台 → 我的训练
3. 找到 `my_lora_girl` 训练任务
4. 下载第 2000 步的模型

**放置位置**:
```
/Users/chenyd11/.openclaw/workspace/stable-diffusion-webui/models/Lora/
```

---

### 3. WD Tagger 模型（提示词反推）
**文件**: `wd-v1-4-moat-tagger-v2.onnx`  
**大小**: ~400MB  
**下载地址**: https://hf-mirror.com/SmilingWolf/wd-v1-4-moat-tagger-v2

**放置位置**:
```
/Users/chenyd11/.openclaw/workspace/stable-diffusion-webui/models/tagger/
```

---

### 4. ControlNet OpenPose（可选）
**文件**: `control_v11p_sd15_openpose.pth`  
**大小**: ~1.4GB  
**下载地址**: https://hf-mirror.com/lllyasviel/ControlNet-v1-1

**放置位置**:
```
/Users/chenyd11/.openclaw/workspace/stable-diffusion-webui/extensions/sd-webui-controlnet/models/
```

---

## 🚀 启动步骤

```bash
# 1. 打开终端
cd /Users/chenyd11/.openclaw/workspace/stable-diffusion-webui

# 2. 启动 SD
./start_mac.sh

# 3. 等待浏览器自动打开
# 地址: http://127.0.0.1:7860
```

---

## 🎨 首次使用配置

### 基础设置（Mac M2 优化）
- **分辨率**: 512×768
- **采样步数**: 25
- **采样器**: DPM++ 2M Karras
- **CFG Scale**: 7

### 提示词模板（写实人像）
```
正向：
1girl, realistic, photo, (best quality:1.2), my_lora_girl,
short bob hair, brown hair, tall, 170cm, slender body, long legs,
[姿势词], [场景词], soft lighting, detailed skin

反向：
(worst quality:1.4), (low quality:1.4), blurry, bad anatomy,
bad hands, text, error, extra digit, fewer digits
```

---

## 📁 已就绪的文件

✅ SD WebUI 软件  
✅ Python 环境 + 依赖  
✅ 启动脚本 `start_mac.sh`  
✅ 高清放大模型 `4x-UltraSharp.pth`  
✅ WD Tagger 扩展  

---

## 💡 快速测试

1. 放入基础模型
2. 启动 SD
3. 文生图标签页
4. 输入提示词生成
5. 成功后下载 LoRA 测试

**遇到问题随时问我！**
