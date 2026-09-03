import io
import os
from pathlib import Path

from docling.datamodel.base_models import FormatToExtensions, InputFormat
from docling.datamodel.document import DocumentStream
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.exceptions import ConversionError
from docling_core.types.doc.base import ImageRefMode

BASE_DIR = Path(__file__).parent

LIBREOFFICE_DIR = BASE_DIR / ".bin" / "LibreOffice" / "App" / "libreoffice" / "program"
os.environ["PATH"] = f"{LIBREOFFICE_DIR}{os.pathsep}{os.environ['PATH']}"

SUPPORTED_EXTS = {
    f".{ext.lower()}" for exts in FormatToExtensions.values() for ext in exts
} & {".pdf", ".docx", ".xlsx", ".xls", ".doc", ".pptx", ".ppt"}
OUTPUT_EXT = ".md"

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=PdfPipelineOptions(
                do_ocr=True,
                ocr_options=RapidOcrOptions(),
                generate_picture_images=True,
            )
        )
    }
)


def _do_convert(src: Path, dst: Path):
    print(f"Convert: [{src}] => [{dst}]")
    converter.convert(
        DocumentStream(name=src.name, stream=io.BytesIO(src.read_bytes()))
    ).document.save_as_markdown(
        dst,
        artifacts_dir=Path(dst.with_suffix(".assets").name),
        image_mode=ImageRefMode.REFERENCED,
    )


def _convert_file(src: Path, dst: Path | None = None) -> Path | None:
    if src.suffix.lower() not in SUPPORTED_EXTS:
        return None
    if dst is None:
        dst = src.with_suffix(OUTPUT_EXT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        _do_convert(src, dst)
    except ConversionError as e:
        print(e)
        return None
    return dst


def _convert_dir(src: Path, dst: Path | None = None) -> list[Path]:
    dst_files = []
    for src_file in src.rglob("*"):
        if dst is not None:
            dst_file = (dst / src_file.relative_to(src)).with_suffix(OUTPUT_EXT)
            dst_file = _convert_file(src_file, dst_file)
        else:
            dst_file = src.with_suffix(OUTPUT_EXT) / src_file.relative_to(
                src
            ).with_suffix(OUTPUT_EXT)
            dst_file = _convert_file(src_file, dst_file)
        if dst_file is not None:
            dst_files.append(dst_file)
    return dst_files


def convert(src: Path | str, dst: Path | str | None = None) -> Path | list[Path] | None:
    src = Path(src)
    if dst is not None:
        dst = Path(dst)
    if src.is_file():
        return _convert_file(src, dst)
    if src.is_dir():
        return _convert_dir(src, dst)
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

    convert(src, dst)
