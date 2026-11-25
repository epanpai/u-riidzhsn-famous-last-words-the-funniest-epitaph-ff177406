#!/usr/bin/env python3
"""Famous Last Words: The Funniest Epitaph — make.fun entry.

Writes a single tombstone epitaph (72 characters) to /output/entry.txt:
the dying words of a man who kept his priorities straight to the end.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import os
import sys

# The entry: one line, 72 characters. It opens with the solemn line every
# dying scene is supposed to have ("Tell my wife I loved her"), then
# undercuts it in the second sentence with the confession he actually
# spent his last breath on ("Tell my boss I never actually read his
# emails"). Two beats, dying speech throughout, a clean twist that lands
# on the last word, and nothing explained: it reads like a line carved
# in stone, short enough to repeat to a friend.
ENTRY = (
    "Tell my wife I loved her. "
    "Tell my boss I never actually read his emails."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-150 characters,
    # not only whitespace, a single line.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 150:
        print(f"entry is {len(text)} characters, over the 150 limit",
              file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte, and that it is still
    # exactly one line (the trailing newline is the only one).
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    if written.count(b"\n") != 1:
        print("verification failed: entry.txt is not a single line",
              file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
