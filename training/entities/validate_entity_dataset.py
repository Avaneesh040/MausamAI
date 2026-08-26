import json
from pathlib import Path

DATA_DIR = Path(__file__).parent

FILES = [
    "train.json",
    "validation.json",
    "test.json",
]


def validate_file(filename):
    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []

    for i, example in enumerate(data):
        text = example["text"]

        for entity in example["entities"]:
            start = entity["start"]
            end = entity["end"]
            label = entity["label"]

            extracted = text[start:end]

            if start < 0 or end > len(text):
                errors.append(
                    f"{filename} example {i}: "
                    f"invalid position {start}:{end}"
                )

            if start >= end:
                errors.append(
                    f"{filename} example {i}: "
                    f"invalid range {start}:{end}"
                )

            if not extracted.strip():
                errors.append(
                    f"{filename} example {i}: "
                    f"empty entity"
                )

            if label == "":
                errors.append(
                    f"{filename} example {i}: "
                    f"empty label"
                )

    print(f"{filename}: {len(data)} examples")

    if errors:
        print(f"❌ {len(errors)} errors")
        for error in errors[:20]:
            print("  ", error)
    else:
        print("✅ All annotations valid")

    return len(errors)


total_errors = 0

print("====================================")
print("ENTITY DATASET VALIDATION")
print("====================================")
print()

for filename in FILES:
    total_errors += validate_file(filename)
    print()

print("====================================")

if total_errors == 0:
    print("✅ DATASET VALIDATION PASSED")
else:
    print(f"❌ DATASET HAS {total_errors} ERRORS")

print("====================================")