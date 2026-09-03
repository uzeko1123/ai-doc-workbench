from pathlib import Path

import pypandoc

BASE_DIR = Path(__file__).parent

TEMPLATE_DOCX = BASE_DIR / ".pandoc" / "template.docx"
if not TEMPLATE_DOCX.is_file():
    TEMPLATE_DOCX = None

PANDOC_FILTER = BASE_DIR / ".pandoc" / "filter.lua"
if not PANDOC_FILTER.is_file():
    PANDOC_FILTER = None

SUPPORTED_EXT = ".md"
OUTPUT_EXT = ".docx"


def _do_export(src: Path, dst: Path):
    print(f"Export: [{src}] => [{dst}]")
    extra_args = [
        f"--resource-path={dst.parent}",
        "--shift-heading-level-by=-1",
        "--columns=1",
    ]
    if TEMPLATE_DOCX is not None:
        extra_args.append(f"--reference-doc={TEMPLATE_DOCX}")
    if PANDOC_FILTER is not None:
        extra_args.append(f"--lua-filter={PANDOC_FILTER}")
    pypandoc.convert_file(
        src, OUTPUT_EXT.lstrip("."), outputfile=dst, extra_args=extra_args
    )


def _export_file(src: Path, dst: Path | None = None) -> Path | None:
    if src.suffix.lower() != SUPPORTED_EXT:
        return None
    if dst is None:
        dst = src.with_suffix(OUTPUT_EXT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        _do_export(src, dst)
    except (RuntimeError, OSError) as e:
        print(e)
        return None
    return dst


def export(src: Path | str, dst: Path | str | None = None) -> Path | None:
    src = Path(src)
    if dst is not None:
        dst = Path(dst)
    if src.is_file():
        return _export_file(src, dst)
    raise ValueError(src)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        src = sys.argv[1]
        dst = None
    elif len(sys.argv) == 3:
        src = sys.argv[1]
        dst = sys.argv[2]
    else:
        raise ValueError("Invalid sys.argv")

    export(src, dst)
