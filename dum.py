from docling.document_converter import DocumentConverter

source = r"D:\Transorg\VAT_2.0\Resume Chatbot\data\p&g overview.pdf"  # Document URL or local path
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())  # Boom! "## Docling Technical Report..."
