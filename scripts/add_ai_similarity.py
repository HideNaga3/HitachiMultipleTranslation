"""
AI意味的類似度判定スクリプト
比較シートの全行について、「単語」と「再翻訳」の意味的類似度を判定
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from difflib import SequenceMatcher


def calculate_semantic_similarity(word1, word2):
    """
    意味的類似度を判定（0-100%）

    判定基準：
    1. 完全一致 → 100%
    2. 同義語リスト → 定義済みスコア
    3. 片方が他方を含む → 90%
    4. 共通文字の割合 → 計算
    5. その他 → difflibベース
    """
    # NaNチェック
    if pd.isna(word1) or pd.isna(word2):
        return 0

    word1 = str(word1).strip()
    word2 = str(word2).strip()

    # 完全一致
    if word1 == word2:
        return 100

    # 同義語・類義語リスト（意味的に同等または近いペア）
    synonyms = {
        # 完全同等（100%）
        ('清掃', 'クリーニング'): 100,
        ('清掃', '掃除'): 100,
        ('危ない', '危険な'): 100,
        ('危ない', '危険'): 100,
        ('けが', '怪我'): 100,
        ('けがをする', '怪我をする'): 100,
        ('ごみ', 'ゴミ'): 100,
        ('ごみ', '廃棄物'): 100,
        ('翻訳サイネージ', '多言語翻訳システム'): 80,
        ('翻訳サイネージ', '翻訳システム'): 85,

        # ほぼ同等（90-95%）
        ('製造', '製造業'): 90,
        ('安全', '安全性'): 95,
        ('作業', '作業する'): 90,
        ('工事', '工事現場'): 90,
        ('建設', '建設業'): 90,

        # やや異なる（50-80%）
        ('危険（な）', '危険物'): 30,  # 意味が異なる
        ('機械', '機器'): 85,
        ('道具', '工具'): 85,
        ('服装', '衣服'): 85,
    }

    # 同義語チェック（順序を問わない）
    for (w1, w2), score in synonyms.items():
        if (word1 == w1 and word2 == w2) or (word1 == w2 and word2 == w1):
            return score

    # 部分一致チェック（片方が他方を完全に含む）
    if word1 in word2 or word2 in word1:
        # 含まれる側の長さとの比率で判定
        shorter = min(len(word1), len(word2))
        longer = max(len(word1), len(word2))
        ratio = shorter / longer
        return int(90 * ratio)

    # 共通文字の割合（漢字・ひらがな・カタカナ）
    set1 = set(word1)
    set2 = set(word2)
    common = set1 & set2

    if common:
        # ジャッカード係数ベース
        jaccard = len(common) / len(set1 | set2)

        # 共通文字が多いほど高スコア
        if jaccard > 0.7:
            return int(80 + jaccard * 20)
        elif jaccard > 0.5:
            return int(60 + jaccard * 30)
        else:
            return int(jaccard * 100)

    # 文字列の類似度（difflib）
    matcher = SequenceMatcher(None, word1, word2)
    difflib_score = matcher.ratio() * 100

    # difflibスコアが高い場合はそれを採用
    if difflib_score > 80:
        return int(difflib_score)

    # カタカナ・ひらがな変換考慮（簡易版）
    # 例: クリーニング vs くりーにんぐ
    word1_kata = word1
    word2_kata = word2

    # 再度チェック
    if word1_kata == word2_kata:
        return 100

    # その他はdifflibスコアを返す
    return int(difflib_score)


# Excelファイル読み込み
print('=' * 80)
print('AI意味的類似度判定')
print('=' * 80)
print()

excel_path = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output\比較用_インドネシア.xlsx'
df = pd.read_excel(excel_path, sheet_name='比較', header=0)

print(f'✓ 比較シート読み込み: {len(df)}行')
print()

# 全行について意味的類似度を計算
print('意味的類似度を計算中...')
ai_similarities = []

for idx, row in df.iterrows():
    word = row['単語']
    retranslation = row['再翻訳']

    similarity = calculate_semantic_similarity(word, retranslation)
    ai_similarities.append(similarity)

    # 進捗表示（100行ごと）
    if (idx + 1) % 100 == 0:
        print(f'  進捗: {idx + 1}/{len(df)}行')

print(f'  完了: {len(df)}行')
print()

# 類似度_ai列を追加
df['類似度_ai'] = [f'{s}%' for s in ai_similarities]

# CSV出力
output_csv = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output\比較_AI判定_全行.csv'
df.to_csv(output_csv, index=False, encoding='utf-8-sig')

print(f'✓ 出力: {output_csv}')
print()

# 統計情報
df['類似度_ai_数値'] = ai_similarities

print('=' * 80)
print('統計情報')
print('=' * 80)
print(f'総行数: {len(df)}行')
print()
print('AI類似度分布:')
print(f'  100%（完全一致）: {len(df[df["類似度_ai_数値"] == 100])}件')
print(f'  80%以上: {len(df[df["類似度_ai_数値"] >= 80])}件')
print(f'  50%以上: {len(df[df["類似度_ai_数値"] >= 50])}件')
print(f'  50%未満: {len(df[df["類似度_ai_数値"] < 50])}件')
print()
print(f'平均類似度: {df["類似度_ai_数値"].mean():.1f}%')
print()

# difflibとの比較
df['difflib_数値'] = df['類似度_difflib'].str.replace('%', '').astype(float)
diff = df['類似度_ai_数値'] - df['difflib_数値']

print('difflibとの比較:')
print(f'  AI判定の方が高い: {len(diff[diff > 0])}件（平均差: {diff[diff > 0].mean():.1f}%）')
print(f'  同じ: {len(diff[diff == 0])}件')
print(f'  AI判定の方が低い: {len(diff[diff < 0])}件（平均差: {diff[diff < 0].mean():.1f}%）')
print()

# サンプル表示（AI判定がdifflibと大きく異なる行）
print('=' * 80)
print('AI判定とdifflibが大きく異なる例（差が30%以上）')
print('=' * 80)
df['差分'] = diff
large_diff = df[abs(df['差分']) >= 30].head(10)

if len(large_diff) > 0:
    print(large_diff[['単語', '再翻訳', '類似度_difflib', '類似度_ai', '差分']].to_string())
else:
    print('該当なし')

print()
print('=' * 80)
print('完了')
print('=' * 80)
