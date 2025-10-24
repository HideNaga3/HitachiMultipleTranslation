"""
2つのクメール語テキストの意味を確認
"""

import sys
from pathlib import Path

# .envからAPIキーを読み込む
sys.path.append(str(Path(__file__).parent.parent))
from dotenv import load_dotenv

# Google Translation API用
sys.path.append(str(Path(__file__).parent.parent / 'scripts_google_translation'))
from scripts.translator import translate_words

# UTF-8出力を強制
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

print("="*80)
print("クメール語テキストの意味確認")
print("="*80)

# 比較する2つのテキスト
text1 = "ការហ្វឹកហ្វឺនជំនាញ"  # pdfplumber
text2 = "ករា ហវឹ្កហវឺ្នជំនញា"  # PyMuPDF

print(f"\n元の日本語: 技能実習")
print(f"\npdfplumber: {text1}")
print(f"PyMuPDF   : {text2}")

# それぞれを日本語に翻訳
print(f"\n" + "="*80)
print("カンボジア語 → 日本語に翻訳")
print("="*80)

try:
    result1 = translate_words([text1], source_lang='km', target_lang='ja')
    result2 = translate_words([text2], source_lang='km', target_lang='ja')

    meaning1 = result1[0] if result1 else '翻訳失敗'
    meaning2 = result2[0] if result2 else '翻訳失敗'

    print(f"\npdfplumber → 日本語:")
    print(f"  {text1}")
    print(f"  ↓")
    print(f"  {meaning1}")

    print(f"\nPyMuPDF → 日本語:")
    print(f"  {text2}")
    print(f"  ↓")
    print(f"  {meaning2}")

    # 比較
    print(f"\n" + "="*80)
    print("結果")
    print("="*80)

    if meaning1 == meaning2:
        print(f"✓ 両方とも同じ意味: 「{meaning1}」")
    else:
        print(f"× 意味が異なります:")
        print(f"  pdfplumber: {meaning1}")
        print(f"  PyMuPDF   : {meaning2}")

    # 元の日本語と比較
    original = "技能実習"
    if meaning1 == original:
        print(f"\n✓ pdfplumberは正確: {meaning1} = {original}")
    else:
        print(f"\n△ pdfplumberは不正確: {meaning1} ≠ {original}")

    if meaning2 == original:
        print(f"✓ PyMuPDFは正確: {meaning2} = {original}")
    else:
        print(f"△ PyMuPDFは不正確: {meaning2} ≠ {original}")

except Exception as e:
    print(f"エラー: {e}")

print("\n" + "="*80)
