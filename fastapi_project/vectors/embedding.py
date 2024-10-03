import faiss
from typing import List
import numpy as np
import requests
import os


class Save_vector():
    def __init__(self,vector,name_file):
        self.__d = 4096
        self.__dir = 'embeddings/'
        self.vector = vector
        self.name_file = name_file


    def make_path(self):
        return self.__dir + self.name_file


    def save(self):
        path = self.make_path()
        index = faiss.IndexFlatL2(self.__d)
        index.add(self.vector)
        faiss.write_index(index, path)


        # Essa parte seria mais no caso de modificar e dar add no index
        # if not os.path.exists(path):
        #     index = faiss.IndexFlatL2(self.__d)
        #     index.add(self.vector)
        #     faiss.write_index(index, path)
        # else:
        #     index = faiss.read_index(path)
        #     if index.d != self.__d:
        #         raise ValueError("dimensions need be equals")
        #     index.add(self.vector)
        #     faiss.write_index(index, path)  
           



def embedding_llama(prompt):
    res = requests.post(url='http://localhost:11434/api/embeddings',
                    json={
                        'model': 'llama3.1',
                        'prompt': prompt
                    })
    return res.json()['embedding']    


def search_vec(prompt):
    embedding = embedding_llama(prompt)
    return np.array([embedding], dtype='float32')


def create_vec(content_txt:List[str],d:int=4096):
    vector = np.zeros(shape=(len(content_txt), d), dtype='float32')
    for i, item in enumerate(content_txt):
        embedding = embedding_llama(item)
        vector[i] = np.array(embedding)
    return vector


####################################


def create_collection(documents, name:str):
    contents = [doc.content for doc in documents]
    vec = create_vec(contents)
    name_collection = name + ".bin"
    Save_vector(vec, name_collection).save()


def remove_collection(name_file: str):
    file_path = 'embeddings/' + name_file + '.bin'
    if os.path.exists(file_path):
        os.remove(file_path)

#####################################

# index = faiss.read_index("index.bin") 

# assuntos = ["Em dezembro vou para praia",
# "precisamos aumentar nossos lucros",
# "O dia está ensolarado",
# "Os custos operacionais foram reduzidos em 20%", 
# "O lançamento para esse primeiro trimestre foi um sucesso!"]

# pesquisa = search_vec("O dia está ensolarado")

# D, I = index.search(pesquisa, 1)

# print(I.flatten(), '\n')

# print("Relevâncias \n")
# print(np.array(assuntos)[I.flatten()], '\n')

#["Em dezembro vou para praia",
# "precisamos aumentar nossos lucros",
# "O dia está ensolarado",
# "os custos operacionais foram reduzidos em 20%", 
# "O lançamento para esse primeiro trimestre foi um sucesso!"]



#fastapi_project\vectors\embedding.py