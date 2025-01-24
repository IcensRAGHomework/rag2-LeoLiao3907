from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import (CharacterTextSplitter,
                                      RecursiveCharacterTextSplitter)

q1_pdf = "OpenSourceLicenses.pdf"
q2_pdf = "勞動基準法.pdf"


def hw02_1(q1_pdf):
    loader = PyPDFLoader(q1_pdf)
    docs = loader.load() # Load as pages
    pages = len(docs)
    print(f"pages: {pages}")

    # This example shows CharacterTextSplitter doesn't use chunk_size and chunk_overlap
    # parameters to split the text.
    spiltter = CharacterTextSplitter(chunk_overlap = 0)
    # Split the last page
    chunks = spiltter.split_documents(docs)
    last_chunk = chunks[-1]
    print(f"last chunk: {last_chunk.metadata}")

    return last_chunk

def hw02_2(q2_pdf):
    result_chunks = []

    # Load pdf
    loader = PyPDFLoader(q2_pdf)
    docs = loader.load() # Load as pages

    # Merge pages to a single text
    content = ""
    for doc in docs:
        content += doc.page_content

    # Split content into title and remaining
    title_paragraph_separators = [r"\n.*第\s*一\s*章.*\n"]
    title_paragraph_splitter = RecursiveCharacterTextSplitter(
        separators = title_paragraph_separators,
        keep_separator = "start",
        chunk_size = 50,
        chunk_overlap = 0,
        is_separator_regex = True)
    title_paragraphs = title_paragraph_splitter.split_text(content)

    if len(title_paragraphs) != 2: # Title and remaining content
        print("Fail to parse title")
        return 0

    title_chunk = title_paragraphs[0]
    remaining_content = title_paragraphs[1]
    result_chunks.append(title_chunk)

    # Split remaining into chapter paragraphs
    chapter_paragraph_separators = [r"(?:\n|^|\s+)第\s*(?:[一二三四五六七八九十百千萬]+|零)\s*章.*\n"]
    chapter_paragraph_splitter = RecursiveCharacterTextSplitter(
        separators = chapter_paragraph_separators,
        keep_separator = "start",
        chunk_size = 500,
        chunk_overlap = 0,
        is_separator_regex = True)
    chapter_paragraphs = chapter_paragraph_splitter.split_text(remaining_content)

    # Split chapter paragraph into sessions
    session_separators = [r"(?:\n|^|\s*)第\s*[0-9]+(?:-[0-9]+)?\s*條.*\n"]
    session_splitter = RecursiveCharacterTextSplitter(
        separators = session_separators,
        keep_separator = "start",
        chunk_size = 50,
        chunk_overlap = 0,
        is_separator_regex = True)
    for chapter in chapter_paragraphs:
        session_chunks = session_splitter.split_text(chapter)
        result_chunks.extend(session_chunks)

    print(f"\nchunks: {len(result_chunks)}")
    # for index, chunk in enumerate(result_chunks):
    #     print(f"chunk: {index + 1}:{chunk}\n{'='*20}\n")+

    return len(result_chunks)
