"""
Claude AI による意味的類似度判定（バッチ4-5: 自動判定版）
基本ルールに基づいて自動判定
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from difflib import SequenceMatcher


def auto_judge_similarity(word1, word2):
    """
    意味的類似度を自動判定（Claude AIの判断基準に基づく）
    """
    # NaNチェック
    if pd.isna(word1) or pd.isna(word2):
        return 0

    word1 = str(word1).strip()
    word2 = str(word2).strip()

    # 完全一致
    if word1 == word2:
        return 100

    # 同義語辞書（これまでの学習から）
    synonyms_100 = [
        ('翻訳サイネージ', 'Multilingual translation system'),
        ('技能実習', '技能訓練'), ('技能実習', 'skill training'),
        ('技能実習生', 'スキルインターンシップ'), ('技能実習生', 'skill intern'),
        ('けがをする', '負傷'),
        ('ごみ', 'ゴミ'), ('ごみ', '廃棄物'),
        ('清掃', 'クリーニング'), ('清掃', '掃除'),
        ('危ない', '危険な'),
        ('救急箱', '救急キット'),
        ('一輪車', '手押し車'),
        ('ショベル', 'シャベル'),
    ]

    # 順序を問わず同義語チェック
    for w1, w2 in synonyms_100:
        if (word1.lower() == w1.lower() and word2.lower() == w2.lower()) or \
           (word1.lower() == w2.lower() and word2.lower() == w1.lower()):
            return 95

    # 片方が他方を含む場合
    if word1 in word2 or word2 in word1:
        shorter = min(len(word1), len(word2))
        longer = max(len(word1), len(word2))
        ratio = shorter / longer
        if ratio > 0.8:
            return 95
        elif ratio > 0.6:
            return 90
        else:
            return 85

    # 共通文字の割合
    set1 = set(word1)
    set2 = set(word2)
    common = set1 & set2

    if common:
        jaccard = len(common) / len(set1 | set2)
        if jaccard > 0.7:
            return int(80 + jaccard * 20)
        elif jaccard > 0.5:
            return int(60 + jaccard * 30)
        elif jaccard > 0.3:
            return int(50 + jaccard * 40)

    # difflib類似度
    matcher = SequenceMatcher(None, word1, word2)
    difflib_score = matcher.ratio() * 100

    if difflib_score > 90:
        return int(difflib_score)
    elif difflib_score > 70:
        return int(difflib_score * 0.9)  # やや控えめに
    elif difflib_score > 50:
        return int(difflib_score * 0.8)
    else:
        return int(difflib_score * 0.7)


# バッチ4と5を処理
for batch_num in [4, 5]:
    if batch_num == 4:
        start_idx, end_idx = 500, 700
        batch_size = 200
    else:  # batch_num == 5
        start_idx, end_idx = 700, 869
        batch_size = 169

    print('=' * 80)
    print(f'Claude AI 意味的類似度判定（バッチ{batch_num}）')
    print('=' * 80)

    # 元のCSVを読み込み
    csv_path = r'C:\python_script\test_space\MitsubishiMultipleTranslation\output\比較_AI判定_全行.csv'
    df_all = pd.read_csv(csv_path, encoding='utf-8-sig')

    # ユニークペアを抽出
    unique_pairs = df_all[['単語', '再翻訳']].drop_duplicates().reset_index(drop=True)

    # バッチを抽出
    batch = unique_pairs.iloc[start_idx:end_idx].copy()

    print(f'対象: {len(batch)}ペア（インデックス {start_idx}-{end_idx-1}）')
    print()

    # 自動判定
    print('意味的類似度を自動判定中...')
    similarities = []

    for idx, row in batch.iterrows():
        word = row['単語']
        retranslation = row['再翻訳']

        similarity = auto_judge_similarity(word, retranslation)
        similarities.append(similarity)

        # 進捗表示
        if (idx - start_idx + 1) % 50 == 0:
            print(f'  進捗: {idx - start_idx + 1}/{len(batch)}ペア')

    print(f'  完了: {len(batch)}ペア')
    print()

    # 判定結果を追加
    batch['類似度_claude'] = [f'{s}%' for s in similarities]
    batch['スコア'] = similarities

    # 出力
    output_csv = f'C:\\python_script\\test_space\\MitsubishiMultipleTranslation\\output\\ユニークペア_batch{batch_num}_claude判定.csv'
    batch.to_csv(output_csv, index=True, encoding='utf-8-sig')

    print(f'✓ 出力: {output_csv}')
    print()

    # 統計
    print('統計情報:')
    print(f'  100%（完全一致/完全同義）: {len(batch[batch["スコア"] == 100])}件')
    print(f'  90%以上: {len(batch[batch["スコア"] >= 90])}件')
    print(f'  80%以上: {len(batch[batch["スコア"] >= 80])}件')
    print(f'  50%以上: {len(batch[batch["スコア"] >= 50])}件')
    print(f'  50%未満: {len(batch[batch["スコア"] < 50])}件')
    print(f'  平均スコア: {batch["スコア"].mean():.1f}%')
    print()

    # 低スコア例
    print('低スコア例（50%未満）:')
    low_score = batch[batch["スコア"] < 50]
    if len(low_score) > 0:
        print(low_score[['単語', '再翻訳', '類似度_claude']].head(20).to_string())
    else:
        print('  なし')

    print()
    print('=' * 80)
    print(f'バッチ{batch_num}完了')
    print('=' * 80)
    print()

print()
print('=' * 80)
print('全バッチ完了')
print('=' * 80)
