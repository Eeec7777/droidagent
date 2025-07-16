# Gemini Models Compatibility Guide

## thinking_config 支援

### 支援的模型
- ✅ `gemini-2.5-flash` - 支援 thinking_config 參數
- ✅ `gemini-2.0-flash-exp` - 支援 thinking_config 參數 (實驗版本)

### 不支援的模型
- ❌ `gemini-1.5-flash` - 不支援 thinking_config 參數
- ❌ `gemini-1.5-pro` - 不支援 thinking_config 參數
- ❌ `gemini-pro` - 不支援 thinking_config 參數
- ❌ `gemini-pro-vision` - 不支援 thinking_config 參數

## 實現細節

在 `droidagent/model.py` 中，我們實現了智能配置：

```python
# Only add thinking_config for newer models that support it
thinking_supported_models = ["gemini-2.5-flash", "gemini-2.0-flash-exp"]
if model in thinking_supported_models:
    config_params['thinking_config'] = types.ThinkingConfig(thinking_budget=0)
```

這樣的實現確保：
1. 新版本模型能夠使用 thinking_config 提升性能
2. 舊版本模型不會因為不支援的參數而出錯
3. 未來新模型可以輕鬆添加到支援列表中

## 如何添加新模型

當 Google 發布新的支援 thinking_config 的模型時，只需要在 `thinking_supported_models` 列表中添加模型名稱即可：

```python
thinking_supported_models = [
    "gemini-2.5-flash", 
    "gemini-2.0-flash-exp",
    "gemini-3.0-flash"  # 新模型
]
```

## 效果

- 📈 **性能提升**: 支援的模型使用優化配置
- 🔧 **兼容性**: 所有模型都能正常運行
- 🔄 **可擴展**: 輕鬆添加新模型支援
- 🚀 **零配置**: 用戶無需關心模型差異
