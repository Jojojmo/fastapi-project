import faiss
import requests
import numpy as np
import os

def search_emb(prompt):
    res = requests.post(url='http://localhost:11434/api/embeddings',
                        json={
                            'model': 'llama3.1',
                            'prompt': prompt
                        })
    embedding = res.json()['embedding']
    return np.array([embedding], dtype='float32')  # Note that the shape is (1, d)


def prompt_engenning(prompt,assunto_relevante):
    body = f'Utilize essa informação: \n {assunto_relevante}. \n' \
           f'Baseado na informação, responda: \n {prompt} \n' 
    return body


def make_guess(prompt):
    res = requests.post(url='http://localhost:11434/api/generate',
                        json={
                            'model': 'llama3.1',
                            'prompt': prompt,
                            'stream': False,
                        })
    return res.json()["response"]


class Call_llama:
    def __init__(self, name_collection, documents_list):
        self.name_collection = name_collection
        self.__path_index = os.path.join('embeddings', name_collection + '.bin')

        self.documents_list = documents_list
        self.index = faiss.read_index(self.__path_index) 


    def similarity(self, prompt):
        relations = search_emb(prompt)
        D, I = self.index.search(relations, 
                                 k=len(self.documents_list))
        return np.array(self.documents_list)[I.flatten()]
    

    def answer(self, prompt):
        similarity = self.similarity(prompt)
        new_prompt = prompt_engenning(prompt=prompt, 
                                      assunto_relevante=similarity)
        return make_guess(new_prompt)


# exp = ['Em dezembro vou para praia', 
#        'Precisamos aumentar nossos lucros', 
#        'O dia está ensolarado', 
#        'Os custos operacionais foram reduzidos em 20%', 
#        'O lançamento para esse primeiro trimestre foi um sucesso!']

# C = Call_llama('teste_llama', exp)

# print(C.answer_llama('O que vou fazer em dezembro?'))