# 天氣預測系統 🌤️

智能天氣預測系統，結合大氣物理公式、多模型集成和自動數據獲取。

## 功能特點

- 📊 **自動數據獲取** - 從 Open-Meteo 免費API主動獲取天氣數據
- 🔬 **大氣物理公式** - 飽和水汽壓、露點溫度、比濕計算
- 🇭🇰 **香港氣候基準** - 30年歷史氣候數據作為預測參考
- 💾 **數據管理** - 自動保存和版本控制
- 📈 **多模型預測** - 氣候平均法 + 物理模型融合

## 快速開始

```python
from weather_system import *

# 獲取香港天氣
fetcher = AutoDataFetcher()
df = fetcher.fetch_hongkong_weather()

# 計算物理量
physics = AtmosphericPhysics()
Td = physics.dew_point(25, 80)
print(f"露點溫度: {Td:.1f}°C")

pip install -r requirements.txt


---

## 📝 操作步驟

1. 點擊 **"Add file"** 按鈕（在頁面右側）
2. 選擇 **"Create new file"**
3. 在文件名輸入框輸入 `requirements.txt`
4. 把上面的內容複製貼上
5. 滾動到頁面底部，點擊綠色的 **"Commit new file"**

然後重複以上步驟，創建 `.gitignore` 和 `README.md`。

---

## 🎯 全部完成後

你的 GitHub 倉庫就會有完整的項目結構：
- `weather-prediction-system.doc`（你已有的）
- `requirements.txt`（依賴列表）
- `.gitignore`（忽略文件）
- `README.md`（項目說明）

需要我幫你生成 `weather_system.py` 的完整代碼嗎？這樣你就可以直接在 GitHub 上編輯了。
