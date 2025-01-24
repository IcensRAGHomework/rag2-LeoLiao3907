from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import (CharacterTextSplitter,
                                      RecursiveCharacterTextSplitter)

q1_pdf = "OpenSourceLicenses.pdf"
q2_pdf = "勞動基準法.pdf"


def hw02_1(q1_pdf):
    print(f"\nhw02_1:")

    # Load pdf
    loader = PyPDFLoader(q1_pdf)
    docs = loader.load() # Load as pages
    print(f"pages: {len(docs)}")

    # This example shows CharacterTextSplitter doesn't use chunk_size and chunk_overlap
    # parameters to split the text.
    spiltter = CharacterTextSplitter(chunk_overlap = 0)
    # Split the last page
    chunks = spiltter.split_documents(docs)
    last_chunk = chunks[-1]
    print(f"last chunk: {last_chunk.metadata}")

    return last_chunk

def hw02_2(q2_pdf):
    print(f"\nhw02_2:")

    # Load pdf
    loader = PyPDFLoader(q2_pdf)
    docs = loader.load() # Load as pages

    # Merge pages to a single text
    full_content = ""
    for doc in docs:
        full_content += doc.page_content

    # print(f"full_content: \n{full_content}\n")

    # Split content into chapter paragraphs
    chapter_paragraph_separators = [r"(?:\n|^|\s*)第\s+(?:[一二三四五六七八九十百千萬]+|零)\s+章.*\n"]
    chapter_paragraph_splitter = RecursiveCharacterTextSplitter(
        separators = chapter_paragraph_separators,
        keep_separator = "start",
        chunk_size = 500,
        chunk_overlap = 0,
        is_separator_regex = True)
    chapter_paragraphs = chapter_paragraph_splitter.split_text(full_content)

    if len(chapter_paragraphs) <= 0:
        print("Fail to parse title")
        return 0

    print(f"chapter_paragraphs (+title): {len(chapter_paragraphs)}")

    # Split chapter paragraph into sessions and put them to total_chunks
    total_chunks = []
    session_separators = [r"(?:\n|^|\s*)第\s+[0-9]+(?:-[0-9]+)?\s+條.*\n"]
    session_splitter = RecursiveCharacterTextSplitter(
        separators = session_separators,
        keep_separator = "start",
        chunk_size = 50,
        chunk_overlap = 0,
        is_separator_regex = True)
    for chapter in chapter_paragraphs:
        session_chunks = session_splitter.split_text(chapter)
        total_chunks.extend(session_chunks)

    print(f"total_chunks: {len(total_chunks)}")
    # for index, chunk in enumerate(total_chunks):
    #     print(f"chunk: {index + 1}:{chunk}\n{'='*20}\n")

    return len(total_chunks)
