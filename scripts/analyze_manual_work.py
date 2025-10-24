"""
手動コピー作業量の分析
"""

import sys
import io
import csv
import re
from pathlib import Path
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("手動コピー作業量の分析")
print("="*80)

# CSVファイル読み込み
csv_path = Path('output') / '全言語統合_テンプレート_インポート用.csv'

# CIDコードのパターン
cid_pattern = re.compile(r'\(cid:\d+\)')

# データ構造
cid_occurrences = defaultdict(list)  # CIDコード別の出現箇所

with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    headers = next(reader)

    for row_idx, row in enumerate(reader, start=2):
        for col_idx, cell in enumerate(row):
            if cid_pattern.search(cell):
                cids = cid_pattern.findall(cell)
                col_name = headers[col_idx] if col_idx < len(headers) else f"列{col_idx+1}"
                ja = row[0] if len(row) > 0 else ''

                for cid in cids:
                    cid_occurrences[cid].append({
                        'row': row_idx,
                        'column': col_name,
                        'ja': ja,
                        'text': cell[:50] + '...' if len(cell) > 50 else cell
                    })

print(f"\nユニークなCIDコード: {len(cid_occurrences)}種類")

# 言語別に分類
cid_by_language = {
    'en': [],
    'th': [],
    'km': [],
    'other': []
}

for cid, occurrences in cid_occurrences.items():
    # 最初の出現箇所の言語で分類
    first_lang = occurrences[0]['column']
    if first_lang in cid_by_language:
        cid_by_language[first_lang].append(cid)
    else:
        cid_by_language['other'].append(cid)

print("\n" + "="*80)
print("言語別CIDコード数")
print("="*80)

for lang, cids in cid_by_language.items():
    if cids:
        print(f"\n{lang}: {len(cids)}種類")

print("\n" + "="*80)
print("作業量シナリオ分析")
print("="*80)

# シナリオ1: 全て手動コピー
print("\n【シナリオ1: 全て手動コピー（最悪ケース）】")
print("-" * 80)

total_unique_cids = len(cid_occurrences)
print(f"コピー回数: {total_unique_cids}回")
print(f"対象セル数: {sum(len(occs) for occs in cid_occurrences.values())}セル")
print(f"推定作業時間: {total_unique_cids * 2}分（1CIDあたり2分想定）")

# シナリオ2: 自動置換可能なものを除外
print("\n【シナリオ2: 簡単なものを自動置換（推奨）】")
print("-" * 80)

# 英語のCID:9（タブ文字）
auto_replaceable = 0
if '(cid:9)' in cid_occurrences:
    auto_replaceable += 1
    en_cells = len(cid_occurrences['(cid:9)'])
    print(f"✓ 英語 (cid:9) → タブ文字: {en_cells}セル自動解決")

manual_cids = total_unique_cids - auto_replaceable
print(f"\n残りのCIDコード: {manual_cids}種類")
print(f"コピー回数: {manual_cids}回")
print(f"推定作業時間: {manual_cids * 2}分（1CIDあたり2分想定）")

# シナリオ3: ToUnicode CMap抽出後
print("\n【シナリオ3: ToUnicode CMap抽出後（最良ケース）】")
print("-" * 80)

# 現在すでに発見されているCID
discovered_cids = {
    545: 'រ',
    559: 'ងា',
    598: 'ោ',
    622: 'ណា',
    630: 'ថ',
    671: 'ភា',
    676: 'ម',
    690: 'ោ',
    814: 'ុ',
    822: 'ើ'
}

already_found = 0
for cid in cid_occurrences.keys():
    cid_num = int(cid.replace('(cid:', '').replace(')', ''))
    if cid_num in discovered_cids:
        already_found += 1

print(f"✓ すでにCMap抽出済み: {already_found}種類")
print(f"✓ 自動置換可能 (cid:9): 1種類")

# 全49ページを調査した場合の推定
estimated_discovery_rate = 0.70  # 70%発見できると仮定
remaining_cids = total_unique_cids - auto_replaceable - already_found
estimated_additional_discovery = int(remaining_cids * estimated_discovery_rate)

final_manual_cids = remaining_cids - estimated_additional_discovery

print(f"\n全49ページCMap調査後の推定:")
print(f"  追加発見CIDコード: {estimated_additional_discovery}種類（推定70%）")
print(f"  最終的な手動コピー: {final_manual_cids}種類")
print(f"  推定作業時間: {final_manual_cids * 2}分")

print("\n" + "="*80)
print("詳細な作業リスト（シナリオ2: 推奨アプローチ）")
print("="*80)

# 自動置換を除いたCIDリスト
manual_work_list = []

for cid, occurrences in sorted(cid_occurrences.items(), key=lambda x: len(x[1]), reverse=True):
    if cid == '(cid:9)':
        continue  # 自動置換可能

    cid_num = int(cid.replace('(cid:', '').replace(')', ''))

    # すでに発見されているか
    status = "✓ CMap発見済み" if cid_num in discovered_cids else "⚠ 手動コピー必要"

    manual_work_list.append({
        'cid': cid,
        'count': len(occurrences),
        'status': status,
        'example': occurrences[0]
    })

print(f"\n手動作業が必要なCIDコード:")
print("-" * 80)

need_manual = [item for item in manual_work_list if "手動コピー必要" in item['status']]

for i, item in enumerate(need_manual[:20], 1):
    example = item['example']
    print(f"\n{i}. {item['cid']} - {item['count']}セルに出現 {item['status']}")
    print(f"   例: 行{example['row']} [{example['column']}] {example['ja']}")
    print(f"       {example['text']}")

if len(need_manual) > 20:
    print(f"\n... 他 {len(need_manual) - 20} 種類")

print("\n" + "="*80)
print("まとめ")
print("="*80)

print(f"""
シナリオ別の作業量:

1. 全て手動コピー（最悪）:
   - コピー回数: {total_unique_cids}回
   - 作業時間: 約{total_unique_cids * 2}分 ({total_unique_cids * 2 / 60:.1f}時間)

2. 簡単なものを自動置換（推奨）:
   - 自動置換: {auto_replaceable}種類（{sum(len(cid_occurrences[cid]) for cid in cid_occurrences if cid == '(cid:9)')}セル解決）
   - 手動コピー: {manual_cids}回
   - 作業時間: 約{manual_cids * 2}分 ({manual_cids * 2 / 60:.1f}時間)

3. 全ページCMap抽出後（最良）:
   - 自動解決: {auto_replaceable + already_found + estimated_additional_discovery}種類（推定）
   - 手動コピー: {final_manual_cids}回（推定）
   - 作業時間: 約{final_manual_cids * 2}分 ({final_manual_cids * 2 / 60:.1f}時間）

【推奨アプローチ】
1. 英語のcid:9をタブに自動置換 → 21セル即座に解決
2. 全49ページToUnicode CMap抽出 → 推定70%自動解決
3. 残り約{final_manual_cids}個のCIDのみPDFから手動コピー
   → 作業時間: 約{final_manual_cids * 2}分（{final_manual_cids * 2 / 60:.1f}時間）
""")

print("="*80)
print("完了")
print("="*80)
