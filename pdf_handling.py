"""
    Class for RAG Architecture : Retrieval-Augmented Generation
    Creation of Vector Database, use embeddings and store them in database.
    Extracting PDF's to Chunks to Embeddings and pass it to our PDF chatting chain.

"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from llm_chains import load_vectordb, create_embeddings
import pypdfium2



def get_pdf_texts(pdfs_in_byte_format):
    return [pdfs_to_text_extraction(pdf_bytes.getvalue()) for pdf_bytes in pdfs_in_byte_format]


def pdfs_to_text_extraction(pdf_bytes):
    pdf_file = pypdfium2.PdfDocument(pdf_bytes)
    return "\n".join(pdf_file.get_page(page_number).get_textpage().get_text_range() for page_number in range(len(pdf_file)))


def create_text_chunks(text):
    # If error : Reduce chunk_size and chunk_overlap.
    splitter = RecursiveCharacterTextSplitter(chunk_size = 512, chunk_overlap=100, separators=["\n","\n\n"])
    return splitter.split_text(text)


def create_document_chunks(text_list):
    documents = []
    for text in text_list :
        text_chunks = create_text_chunks(text)
        for chunk in text_chunks :
            documents.append(Document(page_content=chunk))
    return documents


def add_documents_to_database(pdfs_bytes):
    texts = get_pdf_texts(pdfs_bytes)
    documents = create_document_chunks(texts)
    vector_db = load_vectordb(create_embeddings())
    vector_db.add_documents(documents)
    print("Documents are successfully added to db...")