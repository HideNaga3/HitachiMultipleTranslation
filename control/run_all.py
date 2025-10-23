"""
多言語翻訳プロジェクト - 全処理一括実行
"""
import os
import sys
import subprocess

# プロジェクトルートを取得
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_MAIN = os.path.join(PROJECT_ROOT, 'scripts_main')
VENV_PYTHON = os.path.join(PROJECT_ROOT, '.venv', 'Scripts', 'python.exe')

# 実行順序
EXECUTION_ORDER = [
    {
        'name': 'インポート用CSV + 比較Excel作成',
        'script': 'output_functions.py',
        'args': ['both'],
        'description': 'インポート用CSV + 翻訳・再翻訳シート付きExcelを作成'
    },
    {
        'name': '38列Excelに拡張',
        'script': 'expand_excel_to_38cols.py',
        'description': 'Excelシートを38列に拡張し、空セルを除外した比較シートを作成'
    },
    {
        'name': '類似度スコア追加',
        'script': 'add_similarity_score.py',
        'description': '比較シートに類似度_difflib列と分類を追加'
    },
]


def run_script(script_name, args=None, description="", step_number=None):
    """
    スクリプトを実行

    Parameters:
    -----------
    script_name : str
        実行するスクリプト名
    args : list, optional
        スクリプトの引数
    description : str
        処理の説明
    step_number : int, optional
        ステップ番号（表示用）
    """
    script_path = os.path.join(SCRIPTS_MAIN, script_name)

    if not os.path.exists(script_path):
        print(f"エラー: スクリプトが見つかりません: {script_path}")
        return False

    print()
    print("=" * 80)
    if step_number is not None:
        print(f"[{step_number}/{len(EXECUTION_ORDER)}] {description}")
    else:
        print(f"{description}")
    print("=" * 80)
    print()

    # コマンドを構築
    cmd = [VENV_PYTHON, script_path]
    if args:
        cmd.extend(args)

    # 実行
    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True, capture_output=False)
        print()
        print("OK: 完了")
        print()
        return True
    except subprocess.CalledProcessError as e:
        print()
        print(f"エラー: 処理が失敗しました（終了コード: {e.returncode}）")
        print()
        return False
    except Exception as e:
        print()
        print(f"エラー: {str(e)}")
        print()
        return False


def main():
    """メイン処理"""
    print("=" * 80)
    print("多言語翻訳プロジェクト - 全処理一括実行")
    print("=" * 80)
    print()

    print("実行する処理:")
    for i, step in enumerate(EXECUTION_ORDER, 1):
        print(f"  {i}. {step['name']}")
    print()

    # 確認
    response = input("すべての処理を実行しますか？ (y/n): ").strip().lower()
    if response != 'y':
        print("キャンセルしました。")
        return

    # 実行
    success_count = 0
    failed_count = 0

    for i, step in enumerate(EXECUTION_ORDER, 1):
        args = step.get('args', [])
        success = run_script(step['script'], args, step['description'], step_number=i)

        if success:
            success_count += 1
        else:
            failed_count += 1
            print()
            print("=" * 80)
            print("エラーが発生しました。処理を中断しますか？")
            print("=" * 80)
            print()

            response = input("続行しますか？ (y/n): ").strip().lower()
            if response != 'y':
                break

    # 結果サマリー
    print()
    print("=" * 80)
    print("実行結果サマリー")
    print("=" * 80)
    print()
    print(f"成功: {success_count}件")
    print(f"失敗: {failed_count}件")
    print(f"合計: {len(EXECUTION_ORDER)}件")
    print()


if __name__ == "__main__":
    main()
