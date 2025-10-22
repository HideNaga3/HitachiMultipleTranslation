"""タガログ語XMLファイルからデータを抽出"""
import xml.etree.ElementTree as ET
import pandas as pd
import sys

# ファイル出力にリダイレクト
output_log = open('for_claude/tagalog_xml_extraction.txt', 'w', encoding='utf-8')

xml_file = r'建設関連PDF\【全課統合版】タガログ語_げんばのことば_建設関連職種.xml'

print("=" * 80, file=output_log)
print("タガログ語XMLファイルからのデータ抽出", file=output_log)
print("=" * 80, file=output_log)
print(file=output_log)

# 名前空間を定義
ns = {
    'ss': 'urn:schemas-microsoft-com:office:spreadsheet',
    'o': 'urn:schemas-microsoft-com:office:office',
    'x': 'urn:schemas-microsoft-com:office:excel',
    'html': 'http://www.w3.org/TR/REC-html40'
}

# XMLをパース
tree = ET.parse(xml_file)
root = tree.getroot()

# Worksheetを取得
worksheet = root.find('.//ss:Worksheet', ns)
table = worksheet.find('.//ss:Table', ns)

print(f"Worksheetが見つかりました", file=output_log)
print(file=output_log)

# 全行を抽出
rows = table.findall('.//ss:Row', ns)
print(f"総Row数: {len(rows)}", file=output_log)
print(file=output_log)

# データを抽出
data_rows = []

for row_idx, row in enumerate(rows):
    cells = row.findall('.//ss:Cell', ns)
    row_data = []

    for cell in cells:
        # Cellの Index 属性を確認（空セルスキップ用）
        index_attr = cell.get('{urn:schemas-microsoft-com:office:spreadsheet}Index')

        # データを取得
        data_elem = cell.find('.//ss:Data', ns)
        if data_elem is not None:
            cell_text = ''.join(data_elem.itertext()).strip()
            row_data.append(cell_text)
        else:
            row_data.append('')

    data_rows.append(row_data)

    # 最初の5行を表示
    if row_idx < 5:
        print(f"Row {row_idx}: {row_data[:10]}", file=output_log)

print(file=output_log)
print(f"抽出した総行数: {len(data_rows)}", file=output_log)
print(file=output_log)

# ヘッダー行を特定（"No." を含む行）
header_row_idx = None
for idx, row in enumerate(data_rows):
    if 'No.' in row:
        header_row_idx = idx
        print(f"ヘッダー行を発見: Row {idx}", file=output_log)
        print(f"ヘッダー: {row}", file=output_log)
        break

if header_row_idx is None:
    print("エラー: ヘッダー行が見つかりません", file=output_log)
    output_log.close()
    sys.exit(1)

print(file=output_log)

# ヘッダー行とデータ行を分離
headers = data_rows[header_row_idx]
data_only = data_rows[header_row_idx + 1:]

# 空行を除外
data_only = [row for row in data_only if any(cell != '' for cell in row)]

print(f"データ行数（ヘッダー除外後）: {len(data_only)}", file=output_log)
print(file=output_log)

# DataFrameに変換（列数を揃える）
max_cols = max(len(row) for row in [headers] + data_only)
print(f"最大列数: {max_cols}", file=output_log)

# 各行を最大列数に合わせる
def pad_row(row, target_len):
    return row + [''] * (target_len - len(row))

headers_padded = pad_row(headers, max_cols)
data_padded = [pad_row(row, max_cols) for row in data_only]

# DataFrameを作成
df = pd.DataFrame(data_padded, columns=headers_padded)

print(f"\nDataFrame作成完了", file=output_log)
print(f"行数: {len(df)}", file=output_log)
print(f"列数: {len(df.columns)}", file=output_log)
print(file=output_log)

# 列名を表示
print("列名:", file=output_log)
for i, col in enumerate(df.columns):
    print(f"  {i}: '{col}'", file=output_log)
print(file=output_log)

# 最初の5行を表示
print("データサンプル（最初の5行）:", file=output_log)
print(df.head(5).to_string(index=False), file=output_log)
print(file=output_log)

# CSVに保存
output_file = 'output/【全課統合版】タガログ語_げんばのことば_建設関連職種_from_xml.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"保存完了: {output_file}", file=output_log)
print("=" * 80, file=output_log)

output_log.close()

# コンソールにも結果を表示
print(f"抽出完了: {len(df)}行、{len(df.columns)}列")
print(f"保存先: {output_file}")
