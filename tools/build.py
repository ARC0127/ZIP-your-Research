import os
import re
import sys


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modules_dir = os.path.join(root, "skills", "writing_engine", "modules")
    output_path = os.path.join(root, "skills", "writing_engine", "MASTER_v1.3.2.md")

    pattern = re.compile(r"^\d{2}_.+\.md$")
    modules = [f for f in os.listdir(modules_dir) if pattern.match(f) and not f.startswith("99_")]
    modules.sort()

    if not modules:
        print("No modules found to build.")
        sys.exit(1)

    parts = ["# MASTER v1.3.2 (Writing Engine)\n\n", '> **v1.6.5 binding addendum:** Any visible writing task in ZYR must call `writing_engine`. In the v1.6.5 stack, `writing_engine` is backed by `ext/src/rpws/` (Research-Paper-Writing-Skills) and must use the integrated wrappers `S601`/`S602`/`S603`/`S604` together with `S640` as the global writing and logic gate.\\n\\n', "> **Execution rules:** `boot/11_COMPLETION_FIRST_ANTI_SHORTCUT_v1.5.md` applies after lock activation.\n\n---\n"]
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
