# -*- coding: utf-8 -*-
"""
各言語の実際の列名を表示
"""

import pandas as pd
from pathlib import Path

languages = [
    'カンボジア語',
    'タイ語',
    'ベトナム語',
    'ミャンマー語',
    '中国語',
]

print("各言語の実際の列名:")
print("="*80)

for lang in languages:
    filename = f"output_cleaned/{lang}_cleaned.csv"

    if not Path(filename).exists():
        print(f"\n{lang}: ファイルが見つかりません")
        continue

    df = pd.read_csv(filename, encoding='utf-8-sig')

    print(f"\n{lang} の列名:")
    for i, col in enumerate(df.columns, 1):
        # 翻訳っぽい列を探す
        col_lower = str(col).lower()
        is_translation = any(keyword in col_lower for keyword in [
            'translation', 'terjemahan', 'pagsasalin', 'dịch',
            'ဘာသာ', '词意', '中文', 'របក', 'แปล', '译'
        ]) or 'ြန' in col

        mark = " ← 翻訳候補" if is_translation else ""
        print(f"  {i:2d}. '{col}'{mark}")
