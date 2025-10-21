"""
Document processing pipeline for DefTech AI Document Assistant
Handles PDF and DOCX files, chunking, and embedding generation
"""
import os
import re
from typing import List, Dict, Any
import PyPDF2
from docx import Document
import cohere
import config


class DocumentProcessor:
    """Processes documents for ingestion into vector database"""

    def __init__(self, cohere_client: cohere.ClientV2):
        self.cohere_client = cohere_client

    def load_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load PDF and extract text with page numbers

        Args:
            file_path: Path to PDF file

        Returns:
            List of dicts with 'text' and 'page' keys
        """
        pages = []

        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for page_num, page in enumerate(pdf_reader.pages, start=1):
                    text = page.extract_text()
                    if text.strip():  # Only include non-empty pages
                        pages.append({
                            'text': text.strip(),
                            'page': page_num
                        })

            print(f"✓ Loaded PDF: {os.path.basename(file_path)} ({len(pages)} pages)")
            return pages

        except Exception as e:
            print(f"✗ Error loading PDF {file_path}: {str(e)}")
            return []

    def load_docx(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load DOCX and extract text (paragraph-based page estimation)

        Args:
            file_path: Path to DOCX file

        Returns:
            List of dicts with 'text' and 'page' keys
        """
        pages = []

        try:
            doc = Document(file_path)
            current_page = 1
            paragraphs_per_page = 20  # Rough estimate

            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text.strip())

            # Group paragraphs into estimated pages
            for i in range(0, len(full_text), paragraphs_per_page):
                page_text = "\n".join(full_text[i:i + paragraphs_per_page])
                if page_text:
                    pages.append({
                        'text': page_text,
                        'page': current_page
                    })
                    current_page += 1

            print(f"✓ Loaded DOCX: {os.path.basename(file_path)} (~{len(pages)} pages)")
            return pages

        except Exception as e:
            print(f"✗ Error loading DOCX {file_path}: {str(e)}")
            return []

    def chunk_text(self, text: str, page: int) -> List[Dict[str, Any]]:
        """
        Chunk text into smaller segments with overlap

        Args:
            text: Text to chunk
            page: Page number

        Returns:
            List of chunks with metadata
        """
        # Simple word-based chunking (approximating tokens)
        words = text.split()
        chunks = []

        # Approximate: 1 token ≈ 0.75 words, so 500 tokens ≈ 375 words
        word_chunk_size = int(config.CHUNK_SIZE * 0.75)
        word_overlap = int(config.CHUNK_OVERLAP * 0.75)

        for i in range(0, len(words), word_chunk_size - word_overlap):
            chunk_words = words[i:i + word_chunk_size]
            if chunk_words:  # Avoid empty chunks
                chunks.append({
                    'text': ' '.join(chunk_words),
                    'page': page,
                    'chunk_index': len(chunks)
                })

        return chunks

    def extract_sections(self, text: str) -> str:
        """
        Extract section headers from text (e.g., "1.2.3 Section Title")

        Args:
            text: Text to extract section from

        Returns:
            Section identifier or "General"
        """
        # Look for common section patterns
        patterns = [
            r'^(\d+\.[\d\.]*\s+[A-Z][^\n]{0,50})',  # "1.2.3 Section Title"
            r'^([A-Z][^\n]{0,50}:)',  # "Section Title:"
            r'^(Chapter \d+)',  # "Chapter 1"
        ]

        for pattern in patterns:
            match = re.search(pattern, text[:200], re.MULTILINE)
            if match:
                return match.group(1).strip()

        return "General"

    def process_document(
        self,
        file_path: str,
        manual_name: str,
        classification: str,
        document_type: str,
        metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Process a document into chunks with metadata

        Args:
            file_path: Path to document file
            manual_name: Name of the manual
            classification: Classification level
            document_type: Type (e.g., "manual" or "doctrine")
            metadata: Additional metadata

        Returns:
            List of processed chunks with full metadata
        """
        # Load document based on file extension
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.pdf':
            pages = self.load_pdf(file_path)
        elif ext == '.docx':
            pages = self.load_docx(file_path)
        else:
            print(f"✗ Unsupported file format: {ext}")
            return []

        if not pages:
            return []

        # Process each page into chunks
        all_chunks = []

        for page_data in pages:
            chunks = self.chunk_text(page_data['text'], page_data['page'])

            for chunk in chunks:
                section = self.extract_sections(chunk['text'])

                chunk_metadata = {
                    'manual_name': manual_name,
                    'page': chunk['page'],
                    'section': section,
                    'classification': classification.lower(),
                    'document_type': document_type,
                    'text': chunk['text'],
                    'last_updated': metadata.get('last_updated', '2024') if metadata else '2024'
                }

                # Add any additional metadata
                if metadata:
                    for key, value in metadata.items():
                        if key not in chunk_metadata:
                            chunk_metadata[key] = value

                all_chunks.append(chunk_metadata)

        print(f"✓ Processed {len(all_chunks)} chunks from {manual_name}")
        return all_chunks

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Cohere Embed v3

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        try:
            # Cohere API v2 format
            response = self.cohere_client.embed(
                model=config.COHERE_EMBED_MODEL,
                texts=texts,
                input_type="search_document",  # For indexing documents
                embedding_types=["float"]
            )

            embeddings = response.embeddings.float_
            print(f"✓ Generated {len(embeddings)} embeddings")
            return embeddings

        except Exception as e:
            print(f"✗ Error generating embeddings: {str(e)}")
            return []

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query

        Args:
            query: Search query text

        Returns:
            Embedding vector
        """
        try:
            response = self.cohere_client.embed(
                model=config.COHERE_EMBED_MODEL,
                texts=[query],
                input_type="search_query",  # For search queries
                embedding_types=["float"]
            )

            return response.embeddings.float_[0]

        except Exception as e:
            print(f"✗ Error embedding query: {str(e)}")
            return []


if __name__ == "__main__":
    # Test document processor
    from init_demo import init_cohere_client

    cohere_client = init_cohere_client()
    processor = DocumentProcessor(cohere_client)

    # Test with a sample text
    sample_text = """
    1.2 Equipment Inspection Procedures

    All equipment must be inspected daily before operational use.
    Follow these steps:
    1. Visual inspection for damage
    2. Check all connections and fasteners
    3. Test emergency systems
    4. Document findings in maintenance log
    """

    chunks = processor.chunk_text(sample_text, page=1)
    print(f"\nTest chunking: {len(chunks)} chunks created")
