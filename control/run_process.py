"""
多言語翻訳プロジェクト - 処理実行制御スクリプト
"""
import os
import sys
import subprocess

# プロジェクトルートを取得
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_MAIN = os.path.join(PROJECT_ROOT, 'scripts_main')
VENV_PYTHON = os.path.join(PROJECT_ROOT, '.venv', 'Scripts', 'python.exe')

# 実行可能な処理リスト
PROCESSES = {
    '1': {
        'name': 'インポート用CSV作成（38列）',
        'script': 'output_functions.py',
        'args': ['csv'],
        'description': 'core_filesから38列のインポート用CSVを作成'
    },
    '2': {
        'name': 'インポート用CSV + 比較Excel作成',
        'script': 'output_functions.py',
        'args': ['both'],
        'description': 'CSV + 翻訳・再翻訳・比較シート付きExcelを作成'
    },
    '3': {
        'name': '38列Excelに拡張',
        'script': 'expand_excel_to_38cols.py',
        'args': [],
        'description': 'Excelシートを38列に拡張し、比較シートを作成'
    },
    '4': {
        'name': '類似度スコア追加',
        'script': 'add_similarity_score.py',
        'args': [],
        'description': '比較シートに類似度_difflib列と分類を追加'
    },
    '5': {
        'name': 'シート名変更',
        'script': 'rename_excel_sheets.py',
        'args': [],
        'description': 'Excelシート名を「翻訳」「再翻訳」に変更'
    },
    '6': {
        'name': '比較シート検証',
        'script': 'verify_comparison_sheet.py',
        'args': [],
        'description': '比較シートの内容を確認・統計表示'
    },
    '7': {
        'name': '38列Excel検証',
        'script': 'verify_38cols_excel.py',
        'args': [],
        'description': '38列Excelファイルの内容を検証'
    },
    '8': {
        'name': '類似度例表示',
        'script': 'show_similarity_examples.py',
        'args': [],
        'description': '類似度スコア付き比較シートの例を表示'
    },
    '9': {
        'name': 'ログ保存',
        'script': 'save_project_log.py',
        'args': [],
        'description': 'セッション終了時のログを保存'
    },
    '10': {
        'name': '成果物検証',
        'script': 'verify_deliverables.py',
        'args': [],
        'description': 'CSV/Excelファイルの整合性を自動検証'
    },
}


def display_menu():
    """メニューを表示"""
    print("=" * 80)
    print("多言語翻訳プロジェクト - 処理実行メニュー")
    print("=" * 80)
    print()

    for key, process in sorted(PROCESSES.items()):
        print(f"[{key}] {process['name']}")
        print(f"    {process['description']}")
        print()

    print("[0] 終了")
    print()
    print("=" * 80)


def run_process(process_key):
    """
    指定された処理を実行

    Parameters:
    -----------
    process_key : str
        実行する処理のキー
    """
    if process_key not in PROCESSES:
        print(f"エラー: 無効な処理番号です: {process_key}")
        return False

    process = PROCESSES[process_key]
    script_path = os.path.join(SCRIPTS_MAIN, process['script'])

    if not os.path.exists(script_path):
        print(f"エラー: スクリプトが見つかりません: {script_path}")
        return False

    print()
    print("=" * 80)
    print(f"実行: {process['name']}")
    print("=" * 80)
    print()

    # コマンドを構築
    cmd = [VENV_PYTHON, script_path] + process['args']

    # 実行
    try:
        result = subprocess.run(cmd, cwd=PROJECT_ROOT, check=True, capture_output=False)
        print()
        print("=" * 80)
        print("完了")
        print("=" * 80)
        print()
        return True
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 80)
        print(f"エラー: 処理が失敗しました（終了コード: {e.returncode}）")
        print("=" * 80)
        print()
        return False
    except Exception as e:
        print()
        print("=" * 80)
        print(f"エラー: {str(e)}")
        print("=" * 80)
        print()
        return False


def main():
    """メイン処理"""
    while True:
        display_menu()

        # ユーザー入力
        choice = input("実行する処理の番号を入力してください: ").strip()

        if choice == '0':
            print()
            print("終了します。")
            break

        if choice in PROCESSES:
            success = run_process(choice)
            if success:
                input("\nEnterキーを押して続行...")
        else:
            print()
            print(f"無効な番号です: {choice}")
            print()
            input("Enterキーを押して続行...")


if __name__ == "__main__":
    main()
