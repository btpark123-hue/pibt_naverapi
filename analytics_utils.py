import pandas as pd
import numpy as np
from datetime import datetime

def calculate_ma(df, window_size, column):
    """이동평균(Moving Average) 계산"""
    return df[column].rolling(window=window_size).mean()

def group_by_day_of_week(df):
    """요일별 평균 분석"""
    df_copy = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_copy['Date']):
        df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    
    # 요일 추출 (0=월, 6=일)
    df_copy['day_of_week'] = df_copy['Date'].dt.day_of_week
    days = ['월', '화', '수', '목', '금', '토', '일']
    
    stats = []
    for i, day in enumerate(days):
        day_data = df_copy[df_copy['day_of_week'] == i]
        stats.append({
            'day': day,
            'Gemini': day_data['Gemini_Ratio'].mean() if not day_data.empty else 0,
            'Claude': day_data['Claude_Ratio'].mean() if not day_data.empty else 0
        })
    return pd.DataFrame(stats)

def group_by_period(df, period_type='month'):
    """월별/분기별 합계/평균 분석"""
    df_copy = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df_copy['Date']):
        df_copy['Date'] = pd.to_datetime(df_copy['Date'])
    
    if period_type == 'month':
        df_copy['period'] = df_copy['Date'].dt.strftime('%Y-%m')
    else: # quarter
        df_copy['period'] = df_copy['Date'].dt.to_period('Q').astype(str)
        
    stats = df_copy.groupby('period').agg({
        'Gemini_Ratio': 'mean',
        'Claude_Ratio': 'mean'
    }).reset_index()
    
    stats.columns = ['label', 'Gemini', 'Claude']
    return stats

def calculate_correlation(x, y):
    """상관계수 (Pearson Correlation Coefficient) 계산"""
    if len(x) != len(y) or len(x) == 0:
        return 0
    return np.corrcoef(x, y)[0, 1]
