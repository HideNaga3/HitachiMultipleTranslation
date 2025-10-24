"""
全バッチ統合（手動判定版）
バッチ1-5を統合し、元の1,297行に適用
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd

print('=' * 80)
print('全バッチ統合（手動判定版）')
print('=' * 80)
print()

# 各バッチを読み込み
batches = []
batch_info = [
    (1, 0, 100, 'ユニークペア_batch1_claude判定.csv'),
    (2, 100, 300, 'ユニークペア_batch2_claude判定.csv'),
    (3, 300, 500, 'ユニークペア_batch3_claude判定.csv'),
    (4, 500, 700, 'ユニークペア_batch4_claude判定.csv'),
    (5, 700, 869, 'ユニークペア_batch5_claude判定.csv'),
]

for batch_num, start, end, filename in batch_info:
    filepath = rf'C:\python_script\test_space\MitsubishiMultipleTranslation\output\{filename}'
    df = pd.read_csv(filepath, encoding='utf-8-sig', index_col=0)

    # 列数で判定（3列=batch1-3、4列=batch4-5）
    if len(df.columns) >= 4:
        # バッチ4-5の場合：スコア列（整数）がある
        score_data = df.iloc[:, -1]
    else:
        # バッチ1-3の場合：類似度_claude列（"80%"形式）から抽出
        score_data = df.iloc[:, -1].str.replace('%', '').astype(int)

    print(f'バッチ{batch_num}読み込み: {len(df)}ペア（インデックス {start}-{end-1}）')
    print(f'  平均スコア: {score_data.mean():.1f}%')
    print(f'  100%: {len(score_data[score_data == 100])}件')

    # スコア列を統一
    df['score'] = score_data
    batches.append(df)

print()

# 全バッチを結合
all_unique = pd.concat(batches, ignore_index=False)
all_unique = all_unique.sort_index()

print(f'統合結果: {len(all_unique)}ユニークペア')
print(f'  平均スコア: {all_unique["score"].mean():.1f}%')
print(f'  100%: {len(all_unique[all_unique["score"] == 100])}件')
print(f'  90%以上: {len(all_unique[all_unique["score"] >= 90])}件')
print(f'  80%以上: {len(all_unique[all_unique["score"] >= 80])}件')
print(f'  50%以上: {len(all_unique[all_unique["score"] >= 50])}件')
print(f'  50%未満: {len(all_unique[all_unique["score"] < 50])}件')
print()

# マッピング辞書を作成
mapping = {}
for idx, row in all_unique.iterrows():
    word_col = all_unique.columns[0]  # 単語列
    retrans_col = all_unique.columns[1]  # 再翻訳列
    key = (str(row[word_col]).strip(), str(row[retrans_col]).strip())
    mapping[key] = row['score']

print(f'マッピング辞書作成: {len(mapping)}エントリー')
print()

# 元の全1,297行データに適用
csv_path = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output\比較_AI判定_全行.csv'
df_all = pd.read_csv(csv_path, encoding='utf-8-sig')

print(f'元データ読み込み: {len(df_all)}行')
print()

# 列名を取得
word_col_name = None
retrans_col_name = None
for col in df_all.columns:
    if '単語' in col or 'word' in col.lower():
        word_col_name = col
    if '再翻訳' in col or 'retrans' in col.lower():
        retrans_col_name = col

# Claudeスコアを適用
def get_claude_score(row):
    key = (str(row[word_col_name]).strip(), str(row[retrans_col_name]).strip())
    return mapping.get(key, 50)  # デフォルト50%

df_all['類似度_claude'] = df_all.apply(get_claude_score, axis=1)

# 出力
output_csv = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output\比較_Claude手動判定_全1297行.csv'
df_all.to_csv(output_csv, index=False, encoding='utf-8-sig')

print(f'✓ 出力: {output_csv}')
print()

# 最終統計
print('最終統計（全1,297行）:')
print(f'  平均類似度_claude: {df_all["類似度_claude"].mean():.1f}%')
print(f'  100%: {len(df_all[df_all["類似度_claude"] == 100])}件')
print(f'  90%以上: {len(df_all[df_all["類似度_claude"] >= 90])}件')
print(f'  80%以上: {len(df_all[df_all["類似度_claude"] >= 80])}件')
print(f'  50%以上: {len(df_all[df_all["類似度_claude"] >= 50])}件')
print(f'  50%未満: {len(df_all[df_all["類似度_claude"] < 50])}件')
print()

# difflibとClaudeの比較（文字列から数値に変換）
difflib_col_name = None
for col in df_all.columns:
    if 'difflib' in col.lower():
        difflib_col_name = col
        break

if difflib_col_name:
    # 文字列"%"を除去して数値化
    difflib_scores = df_all[difflib_col_name].astype(str).str.replace('%', '').astype(float)
    print('difflib vs Claude AI:')
    print(f'  difflib平均: {difflib_scores.mean():.1f}%')
    print(f'  Claude平均: {df_all["類似度_claude"].mean():.1f}%')
    print(f'  改善: +{df_all["類似度_claude"].mean() - difflib_scores.mean():.1f}ポイント')
    print()

print('=' * 80)
print('全バッチ統合完了')
print('=' * 80)
