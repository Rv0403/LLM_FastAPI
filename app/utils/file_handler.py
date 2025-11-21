import os
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


def linkdin_text(path_linkedin_pdf):
    """
    Extract text from LinkedIn PDF file.
    
    Args:
        path_linkedin_pdf: Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        ValueError: If the file is not a PDF or is corrupted
    """
    if not os.path.exists(path_linkedin_pdf):
        raise FileNotFoundError(f"PDF file not found: {path_linkedin_pdf}")
    
    # Validate file extension
    file_ext = os.path.splitext(path_linkedin_pdf)[1].lower()
    if file_ext and file_ext != '.pdf':
        raise ValueError(
            f"Expected a PDF file, but got '{file_ext}' file: {path_linkedin_pdf}. "
            f"Please provide a valid PDF file."
        )
    
    try:
        reader = PdfReader(path_linkedin_pdf)
        linkedin = ""
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                linkedin += text
        
        if not linkedin.strip():
            raise ValueError(
                f"PDF file appears to be empty or could not extract text: {path_linkedin_pdf}"
            )
        
        return linkedin
        
    except PdfReadError as e:
        raise ValueError(
            f"Invalid or corrupted PDF file: {path_linkedin_pdf}. "
            f"Error: {str(e)}. Please ensure the file is a valid PDF."
        )
    except Exception as e:
        raise ValueError(
            f"Could not read PDF file {path_linkedin_pdf}: {str(e)}. "
            f"Please ensure the file exists and is a valid PDF."
        )


def summary_text(path_summary_txt):
    """
    Read text from summary file, handling various encodings.
    
    Args:
        path_summary_txt: Path to the text file (.txt)
        
    Returns:
        str: Content of the text file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is not a .txt file or cannot be read
    """
    if not os.path.exists(path_summary_txt):
        raise FileNotFoundError(f"Summary file not found: {path_summary_txt}")
    
    # Validate file extension
    file_ext = os.path.splitext(path_summary_txt)[1].lower()
    if file_ext and file_ext != '.txt':
        raise ValueError(
            f"Expected a .txt file, but got '{file_ext}' file: {path_summary_txt}. "
            f"Please provide a valid text file."
        )
    
    # Try multiple encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(path_summary_txt, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except (FileNotFoundError, PermissionError):
            raise
    
    # Fallback: read with error replacement
    try:
        with open(path_summary_txt, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Could not read file {path_summary_txt}: {str(e)}")