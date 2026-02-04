import os
import re
import sys


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modules_dir = os.path.join(root, "skills", "writing_engine", "modules")
    output_path = os.path.join(root, "skills", "writing_engine", "MASTER_v1.0.1.md")

    pattern = re.compile(r"^\d{2}_.+\.md$")
    modules = [f for f in os.listdir(modules_dir) if pattern.match(f) and not f.startswith("99_")]
    modules.sort()

    if not modules:
        print("No modules found to build.")
        sys.exit(1)

    parts = ["# MASTER v1.0.1 (Writing Engine)\n"]
    for filename in modules:
        path = os.path.join(modules_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            parts.append(f.read().rstrip())
        parts.append("\n\n---\n")

    content = "\n".join(parts).rstrip() + "\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
