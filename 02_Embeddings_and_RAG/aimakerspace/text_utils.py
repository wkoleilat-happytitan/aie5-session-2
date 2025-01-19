import os
from typing import List
import pdfplumber  # Replace PyPDF2 with pdfplumber
from datetime import datetime  # Add this import


class TextFileLoader:
    def __init__(self, path: str, encoding: str = "utf-8"):
        self.documents = []
        self.path = path
        self.encoding = encoding
        self.metadata = []  # Add metadata list

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path):
            if self.path.endswith(".txt"):
                self.load_file()
            elif self.path.endswith(".pdf"):
                self.load_pdf()
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a supported file type (.txt, .pdf)."
            )

    def load_file(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            content = f.read()
            self.documents.append(content)
            self.metadata.append({
                "source": self.path,
                "file_type": "txt",
                "created_date": datetime.fromtimestamp(os.path.getctime(self.path)).isoformat(),
                "modified_date": datetime.fromtimestamp(os.path.getmtime(self.path)).isoformat(),
                "file_size": os.path.getsize(self.path),
                "total_chars": len(content)
            })
            

    def load_pdf(self):
        """Extract text from PDF file using pdfplumber"""
        try:
            with pdfplumber.open(self.path) as pdf:
                text_content = []
                for page in pdf.pages:
                    try:
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
                    except Exception as e:
                        print(f"Warning: Could not extract text from page in {self.path}: {str(e)}")
                        continue
                
                if text_content:
                    full_text = '\n'.join(text_content)
                    self.documents.append(full_text)
                    # Add PDF-specific metadata
                    self.metadata.append({
                        "source": self.path,
                        "file_type": "pdf",
                        "created_date": datetime.fromtimestamp(os.path.getctime(self.path)).isoformat(),
                        "modified_date": datetime.fromtimestamp(os.path.getmtime(self.path)).isoformat(),
                        "file_size": os.path.getsize(self.path),
                        "total_chars": len(full_text),
                        "total_pages": len(pdf.pages)
                    })
                else:
                    print(f"Warning: No text could be extracted from {self.path}")
                    
        except Exception as e:
            print(f"Error reading PDF file {self.path}: {str(e)}")

    def load_directory(self):
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith((".txt", ".pdf")):  # Add PDF support
                    file_path = os.path.join(root, file)
                    if file.endswith(".txt"):
                        with open(file_path, "r", encoding=self.encoding) as f:
                            self.documents.append(f.read())
                    elif file.endswith(".pdf"):
                        self.path = file_path  # Temporarily set path
                        self.load_pdf()

    def load_documents(self):
        self.load()
        return self.documents


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks
    
    def split_with_metadata(self, text: str, metadata: dict) -> List[dict]:
        """Split text and attach metadata to each chunk"""
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk_text = text[i : i + self.chunk_size]
            # Create chunk metadata
            chunk_metadata = {
                **metadata,  # Include original document metadata
                "chunk_index": len(chunks),
                "chunk_start": i,
                "chunk_end": i + len(chunk_text),
                "chunk_size": len(chunk_text)
            }
            chunks.append({
                "text": chunk_text,
                "metadata": chunk_metadata
            })
        return chunks

    def split_texts_with_metadata(self, texts: List[str], metadata_list: List[dict]) -> List[dict]:
        """Split multiple texts with their corresponding metadata"""
        all_chunks = []
        for text, metadata in zip(texts, metadata_list):
            chunks = self.split_with_metadata(text, metadata)
            all_chunks.extend(chunks)
        return all_chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
