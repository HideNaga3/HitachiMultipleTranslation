# -*- coding: utf-8 -*-
"""
各言語の実際の列名をテキストファイルに出力
"""

import pandas as pd
from pathlib import Path

languages = [
    'カンボジア語',
    'タイ語',
    'ベトナム語',
    'ミャンマー語',
    '中国語',
    '英語',
    'インドネシア語',
    'タガログ語',
]

output_file = "for_claude/column_names.txt"
Path("for_claude").mkdir(exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("各言語の実際の列名\n")
    f.write("="*80 + "\n")

    for lang in languages:
        filename = f"output_cleaned/{lang}_cleaned.csv"

        if not Path(filename).exists():
            f.write(f"\n{lang}: ファイルが見つかりません\n")
            continue

        df = pd.read_csv(filename, encoding='utf-8-sig')

        f.write(f"\n{lang} の列名 ({len(df.columns)}列):\n")
        for i, col in enumerate(df.columns, 1):
            # 翻訳っぽい列を探す
            col_lower = str(col).lower()
            is_translation = any(keyword in col_lower for keyword in [
                'translation', 'terjemahan', 'pagsasalin', 'dịch',
                'ဘာသာ', '词意', '中文', 'របក', 'แปล', '译'
            ]) or 'ြန' in col

            mark = " ← 翻訳候補" if is_translation else ""
            f.write(f"  {i:2d}. '{col}'{mark}\n")

print(f"列名を {output_file} に出力しました")
