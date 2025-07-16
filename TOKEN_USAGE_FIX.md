# Token Usage 修復說明

## 問題描述
在使用 Gemini API 時，token 使用統計顯示為 0，這是因為不同版本的 Gemini API 使用不同的屬性名稱來存儲 token 使用信息。

## 解決方案

### 1. 智能屬性檢測
修改了 `APIUsageManager.record_usage()` 和 token 顯示邏輯，支持多種可能的屬性名稱：

```python
# 支持的輸入 token 屬性名稱
possible_input_attrs = ['input_tokens', 'prompt_tokens', 'promptTokens', 'inputTokens']

# 支持的輸出 token 屬性名稱  
possible_output_attrs = ['output_tokens', 'completion_tokens', 'completionTokens', 'outputTokens', 'candidate_tokens']

# 支持的總 token 屬性名稱
possible_total_attrs = ['total_tokens', 'totalTokens']
```

### 2. 自動回退計算
如果找不到 `total_tokens` 屬性，會自動計算：
```python
if total_tokens == 0 and (input_tokens > 0 or output_tokens > 0):
    total_tokens = input_tokens + output_tokens
```

### 3. 調試信息
當無法找到 token 信息時，會顯示調試信息：
```
⚠️  No token usage found in response metadata
   Available attributes: ['input_tokens', 'output_tokens', ...]
   Raw metadata: <metadata object>
```

## 支持的 API 版本

### Google GenAI API v1.x
- `input_tokens`
- `output_tokens`
- `total_tokens`

### Google GenAI API v2.x (如果存在)
- `prompt_tokens`
- `completion_tokens`
- `promptTokens`
- `completionTokens`
- `inputTokens`
- `outputTokens`
- `candidate_tokens`

## 測試結果
通過模擬測試確認支持所有可能的屬性名稱結構：
- ✅ `input_tokens` + `output_tokens`
- ✅ `prompt_tokens` + `completion_tokens`
- ✅ `total_tokens` 僅有總數
- ✅ 混合結構自動處理
- ✅ 空結構顯示調試信息

## 使用建議
1. 如果遇到 token 顯示為 0 的問題，查看調試信息
2. 檢查 `Available attributes` 來確認實際的屬性名稱
3. 如果有新的屬性名稱，可以添加到支持列表中

## 向後兼容性
此修復完全向後兼容，不會影響現有的正常工作的 API 調用。
