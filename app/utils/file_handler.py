from io import BytesIO
from typing import Union

from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


def linkdin_text(pdf_bytes: Union[bytes, bytearray], filename: str):
    """
    Extract text from LinkedIn PDF file.
    
    Args:
        pdf_bytes: PDF file content as bytes
        filename: Name of the PDF file
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        ValueError: If the file is not a PDF or is corrupted
    """
    if not isinstance(pdf_bytes, (bytes, bytearray)):
        raise TypeError("PDF content must be bytes-like object.")

    if not filename.lower().endswith('.pdf'):
        raise ValueError(
            f"Expected a PDF file, but got '{filename}'. "
            f"Please provide a valid PDF file."
        )

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        return _extract_pdf_text(reader)
    except PdfReadError as e:
        raise ValueError(
            f"Invalid or corrupted PDF file: {filename}. "
            f"Error: {str(e)}. Please ensure the file is a valid PDF."
        )
    except Exception as e:
        raise ValueError(
            f"Could not read PDF file {filename}: {str(e)}. "
            f"Please ensure the file is a valid PDF."
        )


def summary_text(text_bytes: Union[bytes, bytearray], filename: str):
    """
    Read text from summary file, handling various encodings.
    
    Args:
        text_bytes: Text file content as bytes
        filename: Name of the text file
        
    Returns:
        str: Content of the text file
        
    Raises:
        ValueError: If the file is not a .txt file or cannot be read
    """
    if not isinstance(text_bytes, (bytes, bytearray)):
        raise TypeError("Summary content must be bytes-like object.")

    if not filename.lower().endswith('.txt'):
        raise ValueError(
            f"Expected a .txt file, but got '{filename}'. "
            f"Please provide a valid text file."
        )

    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

    for encoding in encodings:
        try:
            return text_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue

    try:
        return text_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        raise ValueError(f"Could not read file {filename}: {str(e)}")


def _extract_pdf_text(reader: PdfReader) -> str:
    linkedin = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text

    if not linkedin.strip():
        raise ValueError("PDF file appears to be empty or could not extract text.")

    return linkedin