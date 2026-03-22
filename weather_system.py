"""
天氣預測系統 - 完整版
包含數據管理、大氣物理公式、自動數據獲取
"""

import os
import json
import numpy as np
import pandas as pd
import requests
import math
from datetime import datetime, timedelta

print("=" * 60)
print("🌤️ 天氣預測系統 v3.0")
print("=" * 60)

# ==================== 數據管理器 ====================
class WeatherDataManager:
    def __init__(self):
        self.data_dir = 'data'
        self.metadata_file = 'data_metadata.json'
        os.makedirs(self.data_dir, exist_ok=True)
        self.metadata = self._load_metadata()
        print("✅ 數據管理器初始化完成")
    
    def _load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {'datasets': {}, 'total_records': 0}
    
    def save_dataset(self, df, name, source='api'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.parquet"
        filepath = os.path.join(self.data_dir, filename)
        df.to_parquet(filepath, index=False)
        print(f"✅ 保存: {name} ({len(df)} 條記錄)")
        return filepath

# ==================== 大氣物理公式 ====================
class AtmosphericPhysics:
    def saturation_vapor_pressure(self, T):
        """飽和水汽壓 (Tetens公式)"""
        return 6.112 * math.exp(17.67 * T / (T + 243.5))
    
    def dew_point(self, T, RH):
        """露點溫度"""
        e = self.saturation_vapor_pressure(T) * RH / 100
        if e <= 0:
            return T - 10
        ln_term = math.log(e / 6.112)
        return (243.5 * ln_term) / (17.67 - ln_term)
    
    def specific_humidity(self, T, P, RH):
        """比濕"""
        e = self.saturation_vapor_pressure(T) * RH / 100
        epsilon = 0.622
        return epsilon * e / (P - (1 - epsilon) * e)

# ==================== 自動數據獲取 ====================
class AutoDataFetcher:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def fetch_hongkong_weather(self):
        """從 Open-Meteo 獲取香港天氣"""
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    'latitude': 22.3193,
                    'longitude': 114.1694,
                    'current_weather': True,
                    'hourly': 'temperature_2m,relativehumidity_2m',
                    'forecast_days': 7
                },
                timeout=15
            )
            if response.status_code == 200:
                data = response.json()
                processed = []
                if 'current_weather' in data:
                    current = data['current_weather']
                    processed.append({
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'temperature': current.get('temperature', 20.0),
                        'wind_speed': current.get('windspeed', 3.0),
                        'source': 'open_meteo'
                    })
                if processed:
                    df = pd.DataFrame(processed)
                    self.data_manager.save_dataset(df, 'hongkong_weather', 'open_meteo')
                    return df
        except Exception as e:
            print(f"獲取失敗: {e}")
        return None

# ==================== 香港氣候基準 ====================
HONGKONG_CLIMATE = {
    1: {'avg_temp': 15.6, 'rainfall': 36, 'humidity': 70},
    2: {'avg_temp': 17.1, 'rainfall': 53, 'humidity': 76},
    3: {'avg_temp': 19.6, 'rainfall': 78, 'humidity': 79},
    4: {'avg_temp': 22.7, 'rainfall': 132, 'humidity': 84},
    5: {'avg_temp': 25.4, 'rainfall': 217, 'humidity': 86},
    6: {'avg_temp': 27.1, 'rainfall': 322, 'humidity': 87},
    7: {'avg_temp': 27.6, 'rainfall': 263, 'humidity': 85},
    8: {'avg_temp': 27.4, 'rainfall': 311, 'humidity': 86},
    9: {'avg_temp': 28.6, 'rainfall': 225, 'humidity': 82},
    10: {'avg_temp': 24.5, 'rainfall': 75, 'humidity': 74},
    11: {'avg_temp': 21.0, 'rainfall': 47, 'humidity': 71},
    12: {'avg_temp': 16.7, 'rainfall': 37, 'humidity': 65}
}

def get_hk_climate(month):
    return HONGKONG_CLIMATE.get(month, HONGKONG_CLIMATE[1])

# ==================== 運行測試 ====================
if __name__ == "__main__":
    print("\n🚀 啟動天氣系統測試")
    print("-" * 40)
    
    # 創建數據管理器
    dm = WeatherDataManager()
    
    # 創建數據獲取器
    fetcher = AutoDataFetcher(dm)
    
    # 獲取香港天氣
    print("\n📡 獲取香港天氣...")
    df = fetcher.fetch_hongkong_weather()
    
    if df is not None:
        print(df)
    
    # 測試物理公式
    print("\n🔬 測試物理公式")
    physics = AtmosphericPhysics()
    Td = physics.dew_point(25, 80)
    print(f"溫度25°C、濕度80%時的露點: {Td:.1f}°C")
    
    # 測試氣候數據
    print("\n🇭🇰 香港氣候基準")
    current_month = datetime.now().month
    climate = get_hk_climate(current_month)
    print(f"當前月份 {current_month}月: 平均溫度 {climate['avg_temp']}°C")
    
    print("\n✅ 系統測試完成!")
