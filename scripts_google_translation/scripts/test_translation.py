"""
日本語→英語の翻訳テスト（20単語）
"""
from translator import translate_words
import csv
from pathlib import Path
from datetime import datetime


def main():
    # 翻訳する日本語の単語リスト（8文字以内）
    japanese_words = [
        "平和",
        "希望",
        "未来",
        "勇気",
        "友情",
        "愛情",
        "自由",
        "正義",
        "幸福",
        "知恵",
        "真実",
        "美しさ",
        "強さ",
        "優しさ",
        "誠実",
        "調和",
        "創造",
        "成長",
        "信頼",
        "感謝"
    ]

    print("=" * 60)
    print("日本語→英語 翻訳テスト（20単語）")
    print("=" * 60)
    print(f"\n開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"翻訳単語数: {len(japanese_words)}語\n")

    try:
        # 翻訳実行
        print("翻訳中...")
        english_translations = translate_words(
            japanese_words,
            source_lang="ja",
            target_lang="en"
        )

        # 結果表示
        print("\n[翻訳結果]")
        print("-" * 60)
        results = []
        for i, (ja, en) in enumerate(zip(japanese_words, english_translations), 1):
            print(f"{i:2d}. {ja:8s} → {en}")
            results.append({
                "No": i,
                "日本語": ja,
                "英語": en
            })

        # CSV出力
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = output_dir / f"translation_test_{timestamp}.csv"

        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["No", "日本語", "英語"])
            writer.writeheader()
            writer.writerows(results)

        print("-" * 60)
        print(f"\n[OK] 翻訳完了")
        print(f"CSV出力: {csv_file}")
        print(f"終了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"\n[ERROR] 翻訳エラーが発生しました: {e}")
        return 1

    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())
