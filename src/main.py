import os
from extract_text import read_file_as_text
from vector import convert_to_vector
from vector import find_relevant_chunk
from langchain.schema import Document
from ask_llm import call_llm


from extract_text import read_file_as_text

n= int(input("Enter num of files to analyse: "))

all_content= []

for i in range(n):
    file_path= (input("enter file path: "))
    content = read_file_as_text(file_path)
    #print(f"The file is of type: {document_type}")
    all_content.append(Document(page_content=content)) 

vector_store= convert_to_vector(all_content)

while True:
    query = input("enter your query (or type 'quit' to exit): ").strip()
    if query.lower() in ["quit", "exit", "q"]:
        print("Exiting query loop. Cheers.")
        break

    ans = find_relevant_chunk(query, vector_store)
   # print(ans)
    sol= call_llm(query, ans)
    print(sol)

    #all good, have to convert to ipynb