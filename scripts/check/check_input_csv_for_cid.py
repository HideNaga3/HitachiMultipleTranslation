"""
入力CSVにCIDコードがあるかチェック
"""
import pandas as pd
import os

output_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output'
for_claude_dir = r'C:\python_script\test_space\MitsubishiMultipleTranslation\for_claude'
input_csv = os.path.join(output_dir, '全言語統合_テンプレート_インポート用.csv')

# CSV読み込み
df = pd.read_csv(input_csv, encoding='utf-8-sig')

output_lines = []

output_lines.append("=" * 80)
output_lines.append("入力CSVのCIDコード確認")
output_lines.append("=" * 80)
output_lines.append("")

# 各言語列でCIDコードを検出
cid_count = 0
for col in ['en', 'fil-PH', 'zh', 'th', 'vi', 'my', 'id', 'km']:
    col_cid_count = df[col].astype(str).str.contains(r'\(cid:', na=False).sum()
    if col_cid_count > 0:
        output_lines.append(f"{col:10s}: {col_cid_count}件のCIDコード検出")
        cid_count += col_cid_count

        # サンプル表示
        cid_rows = df[df[col].astype(str).str.contains(r'\(cid:', na=False)]
        output_lines.append(f"  サンプル（{col}）:")
        for idx, row in cid_rows.head(5).iterrows():
            output_lines.append(f"    行{idx}: {repr(row[col][:100])}")
        output_lines.append("")

if cid_count == 0:
    output_lines.append("CIDコードは検出されませんでした")
else:
    output_lines.append(f"合計: {cid_count}件のCIDコード検出")
    output_lines.append("")
    output_lines.append("結論: CIDコードは入力CSV自体に存在します（PDF抽出時から存在）")
    output_lines.append("これはPDFからの抽出プロセスでCIDコードが含まれたためです。")

output_lines.append("=" * 80)

# ファイルに保存
output_file = os.path.join(for_claude_dir, 'input_csv_cid_check.txt')
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"確認結果を保存: {output_file}")
print(f"CIDコード検出数: {cid_count}件")
