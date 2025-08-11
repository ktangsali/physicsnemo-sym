import os
import re
from pathlib import Path

project_root = Path(__file__).parent.resolve()
image_dir = project_root / "images"

pattern = re.compile(r"(?<=\.\. figure:: )/images/([^\s]+)")

for rst_path in project_root.rglob("*.rst"):
    rst_dir = rst_path.parent
    updated_lines = []

    with open(rst_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    changed = False
    for line in lines:
        match = pattern.search(line)
        if match:
            image_subpath = match.group(1)
            full_image_path = image_dir / image_subpath
            try:
                relative_path = os.path.relpath(full_image_path, start=rst_dir)
                new_line = pattern.sub(relative_path.replace("\\", "/"), line)
                updated_lines.append(new_line)
                changed = True
            except Exception as e:
                print(f"Warning: Could not resolve relative path for {full_image_path}: {e}")
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    if changed:
        with open(rst_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        print(f"✅ Updated: {rst_path.relative_to(project_root)}")

