#!/usr/bin/env python3
import os, sys, json, re

INDEX_HTML = "index.html"
DOC_ROOT   = "d"
GHPAGES_URL= "https://whompinc.github.io/Files/"

def build_tree(path):
    tree = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            tree[name] = build_tree(full)
        else:
            tree[name] = "file"
    return tree

def inject_tree(html, tree_json):
    pattern = re.compile(r"(const\s+treeData\s*=\s*)(\{[\s\S]*?\})(;)")
    return pattern.sub(r"\1" + tree_json + r"\3", html, count=1)

def cmd_map(root):
    tree = {
        "C:": build_tree(root),
        "VIRTUAL:": {}
    }
    tree_json = json.dumps(tree, indent=2)
    html = open(INDEX_HTML, encoding="utf8").read()
    new_html = inject_tree(html, tree_json)
    with open(INDEX_HTML, "w", encoding="utf8") as f:
        f.write(new_html)
    print(f"✅ {INDEX_HTML} updated")

def cmd_open():
    print(GHPAGES_URL)

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: python file_master.py map [PATH] | open")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd in ("map", ".map"):
        root = sys.argv[2] if len(sys.argv)>2 else DOC_ROOT
        if not os.path.isdir(root):
            print(f"Error: {root} is not a directory.")
            sys.exit(1)
        cmd_map(root)
    elif cmd=="open":
        cmd_open()
    else:
        print("Unknown command.")
