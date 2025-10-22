"""タガログ語XMLファイルの構造を分析"""
import xml.etree.ElementTree as ET
import sys

# ファイル出力にリダイレクト
sys.stdout = open('for_claude/tagalog_xml_analysis.txt', 'w', encoding='utf-8')

xml_file = r'建設関連PDF\【全課統合版】タガログ語_げんばのことば_建設関連職種.xml'

print("=" * 80)
print("タガログ語XMLファイルの分析")
print("=" * 80)
print()

# XMLをパース
tree = ET.parse(xml_file)
root = tree.getroot()

print(f"ルート要素: {root.tag}")
print(f"ルート属性: {root.attrib}")
print()

# 子要素を確認
print("【ルート直下の子要素】")
for i, child in enumerate(root):
    print(f"{i}: タグ={child.tag}, 属性={child.attrib}, テキスト={child.text[:50] if child.text else 'None'}...")
    if i >= 5:
        print(f"... 以下省略 (総数: {len(list(root))})")
        break
print()

# 最初の要素を詳細に調査
if len(list(root)) > 0:
    print("【最初の要素の詳細構造】")
    first_elem = list(root)[0]

    def print_element(elem, indent=0):
        prefix = "  " * indent
        text = elem.text[:100] if elem.text and elem.text.strip() else ""
        print(f"{prefix}<{elem.tag}> {elem.attrib} = {text}")
        for child in elem:
            print_element(child, indent + 1)

    print_element(first_elem)
    print()

# データ行っぽい要素を探す
print("【データ構造の推測】")
# よくあるXML構造を探索
for possible_row_tag in ['row', 'record', 'item', 'entry', 'data', 'table', 'page']:
    rows = root.findall(f".//{possible_row_tag}")
    if rows:
        print(f"'{possible_row_tag}'要素が {len(rows)} 個見つかりました")

        if len(rows) > 0:
            print(f"\n最初の '{possible_row_tag}' 要素:")
            print_element(rows[0], 1)
            print()

# 全体の統計
print("=" * 80)
print("【統計情報】")
print(f"総要素数: {len(list(root.iter()))}")

# すべてのタグ名を収集
all_tags = {}
for elem in root.iter():
    tag = elem.tag
    if tag not in all_tags:
        all_tags[tag] = 0
    all_tags[tag] += 1

print(f"\nユニークなタグ数: {len(all_tags)}")
print("\nタグの出現回数:")
for tag, count in sorted(all_tags.items(), key=lambda x: -x[1])[:20]:
    print(f"  {tag}: {count}回")

print()
print("=" * 80)
