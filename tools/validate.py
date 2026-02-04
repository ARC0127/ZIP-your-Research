import glob
import os
import re
import sys


FRONT_MATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_front_matter(text):
    match = FRONT_MATTER_PATTERN.match(text)
    if not match:
        return None
    raw = match.group(1)
    data = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_path = os.path.join(root, "skills")
    pattern = os.path.join(skills_path, "**", "*.md")
    files = glob.glob(pattern, recursive=True)
    ids = {}
    errors = []

    for path in files:
        filename = os.path.basename(path)
        if not filename.startswith("S"):
            continue
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        front = parse_front_matter(text)
        if front is None:
            errors.append(f"Missing YAML front matter: {path}")
            continue
        for key in ("id", "name", "category"):
            if key not in front or not front[key]:
                errors.append(f"Missing '{key}' in front matter: {path}")
        skill_id = front.get("id")
        if skill_id:
            if skill_id in ids:
                errors.append(f"Duplicate id '{skill_id}': {path} and {ids[skill_id]}")
            else:
                ids[skill_id] = path

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()
