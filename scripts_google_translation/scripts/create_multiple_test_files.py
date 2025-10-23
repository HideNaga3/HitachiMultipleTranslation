"""
複数ファイル一括翻訳テスト用のファイルを作成
同じ構造のCSV/Excelファイルを複数作成する
"""
import csv
from pathlib import Path
from openpyxl import Workbook


def create_multiple_csv_files():
    """同じ構造のCSVファイルを3つ作成"""
    test_data_dir = Path(__file__).parent.parent / "test_data"
    test_data_dir.mkdir(exist_ok=True)

    # データセット1: 感情
    data1 = ["喜び", "悲しみ", "怒り", "恐怖", "驚き"]

    # データセット2: 自然
    data2 = ["太陽", "月", "星", "海", "山"]

    # データセット3: 色
    data3 = ["赤", "青", "緑", "黄", "白"]

    datasets = [
        ("emotions.csv", data1),
        ("nature.csv", data2),
        ("colors.csv", data3)
    ]

    created_files = []
    for filename, data in datasets:
        filepath = test_data_dir / filename
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["日本語"])  # ヘッダー
            for word in data:
                writer.writerow([word])
        created_files.append(str(filepath))
        print(f"[作成] {filepath}")

    return created_files


def create_multiple_excel_files():
    """同じ構造のExcelファイルを3つ作成"""
    test_data_dir = Path(__file__).parent.parent / "test_data"
    test_data_dir.mkdir(exist_ok=True)

    # データセット1: 動物
    data1 = ["犬", "猫", "鳥", "魚", "馬"]

    # データセット2: 食べ物
    data2 = ["米", "パン", "肉", "魚", "野菜"]

    # データセット3: 天気
    data3 = ["晴れ", "雨", "曇り", "雪", "風"]

    datasets = [
        ("animals.xlsx", data1),
        ("foods.xlsx", data2),
        ("weather.xlsx", data3)
    ]

    created_files = []
    for filename, data in datasets:
        filepath = test_data_dir / filename
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        # ヘッダー
        ws.append(["日本語"])

        # データ
        for word in data:
            ws.append([word])

        wb.save(filepath)
        created_files.append(str(filepath))
        print(f"[作成] {filepath}")

    return created_files


if __name__ == "__main__":
    print("=" * 70)
    print("複数ファイル一括翻訳テスト用ファイル作成")
    print("=" * 70)

    print("\n[1] CSVファイル作成中...")
    csv_files = create_multiple_csv_files()
    print(f"\n作成完了: {len(csv_files)}ファイル")
    for f in csv_files:
        print(f"  - {Path(f).name}")

    print("\n[2] Excelファイル作成中...")
    excel_files = create_multiple_excel_files()
    print(f"\n作成完了: {len(excel_files)}ファイル")
    for f in excel_files:
        print(f"  - {Path(f).name}")

    print("\n" + "=" * 70)
    print("全ファイル作成完了")
    print("=" * 70)
