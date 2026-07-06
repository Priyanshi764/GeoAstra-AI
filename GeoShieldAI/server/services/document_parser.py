"""
Document Parser for GeoShield AI
Parses various document formats (PDF, CSV, TXT, JSON, DOCX)
"""
import csv
import json
import io
from pathlib import Path
import PyPDF2
from docx import Document as DocxDocument

class DocumentParser:
    """Parses different document formats"""
    
    @staticmethod
    def parse_csv(file_content):
        """Parse CSV file"""
        try:
            if isinstance(file_content, bytes):
                file_content = file_content.decode('utf-8')
            
            reader = csv.DictReader(io.StringIO(file_content))
            data = list(reader)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def parse_pdf(file_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text()
            
            return {"success": True, "text": text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def parse_txt(file_path):
        """Parse text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                text = txt_file.read()
            
            return {"success": True, "text": text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def parse_json(file_content):
        """Parse JSON file"""
        try:
            if isinstance(file_content, bytes):
                file_content = file_content.decode('utf-8')
            
            data = json.loads(file_content)
            return {"success": True, "data": data}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def parse_docx(file_path):
        """Extract text from DOCX file"""
        try:
            doc = DocxDocument(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return {"success": True, "text": text}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    @staticmethod
    def parse_file(file_path, file_type):
        """
        Parse file based on type
        Supported types: pdf, csv, txt, json, docx
        """
        file_type = file_type.lower()
        
        if file_type == "pdf":
            return DocumentParser.parse_pdf(file_path)
        elif file_type == "csv":
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return DocumentParser.parse_csv(content)
        elif file_type == "txt":
            return DocumentParser.parse_txt(file_path)
        elif file_type == "json":
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return DocumentParser.parse_json(content)
        elif file_type == "docx":
            return DocumentParser.parse_docx(file_path)
        else:
            return {"success": False, "message": f"Unsupported file type: {file_type}"}
    
    @staticmethod
    def extract_text_from_csv_rows(rows):
        """Convert CSV rows to searchable text"""
        text_parts = []
        for row in rows:
            for key, value in row.items():
                if value:
                    text_parts.append(f"{key}: {value}")
        return " ".join(text_parts)
    
    @staticmethod
    def extract_text_from_json(data):
        """Convert JSON data to searchable text"""
        if isinstance(data, dict):
            text_parts = []
            for key, value in data.items():
                text_parts.append(f"{key}: {str(value)}")
            return " ".join(text_parts)
        elif isinstance(data, list):
            text_parts = []
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        text_parts.append(f"{key}: {str(value)}")
            return " ".join(text_parts)
        else:
            return str(data)
