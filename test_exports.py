from services.exporter import docx_bytes, pdf_bytes, latex_source, project_zip

def test_exports_return_bytes():
    paper = "# Demo\n## Introduction\nA simple test paragraph."
    assert docx_bytes("Demo", paper).startswith(b"PK")
    assert pdf_bytes("Demo", paper).startswith(b"%PDF")
    assert b"\\documentclass" in latex_source("Demo", paper)
    assert project_zip("Demo", paper, []).startswith(b"PK")
