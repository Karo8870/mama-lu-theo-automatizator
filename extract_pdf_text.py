import argparse
import sys

import fitz  # PyMuPDF


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    try:
        texts = []
        for page in doc:
            page_text = page.get_text("text")
            texts.append(page_text)
        return "\n".join(texts)
    finally:
        doc.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    args = parser.parse_args()

    try:
        text = extract_pdf_text(args.pdf_path)
    except Exception as exc:  # noqa: BLE001
        print(f"Error reading PDF: {exc}", file=sys.stderr)
        sys.exit(1)

    print(text)


if __name__ == "__main__":
    main()

