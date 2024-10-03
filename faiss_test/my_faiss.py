#Site do Llama
#https://ollama.com/
#Vídeo base
#https://www.youtube.com/watch?v=8L3tGcYc774
#Documentação da API:
#https://github.com/ollama/ollama/blob/main/docs/api.md

import faiss
import numpy as np
import requests

d = 4096

def create_emb(d, content_txt):
    vector = np.zeros(shape=(len(content_txt), d), dtype='float32')
    for i, item in enumerate(content_txt):
        res = requests.post(url='http://localhost:11434/api/embeddings',
                            json={
                                'model': 'llama3.1',
                                'prompt': item
                            })
        embedding = res.json()['embedding']
        vector[i] = np.array(embedding)
    return vector

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
                            'stream': False
                        })
    return res.json()["response"]



index = faiss.IndexFlatL2(d)

assuntos = [
    'Para falar de seguros, use o telefone da Tokio Marine: 0800 703 9000',
    'Ligue para este telefone: 0800-749-0029 de SAC da Movida para fazer reclamações ou tentar resolver problemas de alocações de veículos',
    'Para compra de pneus acesse o site da Michelin: https://www.michelin.com.br/',
    'Encontre carros Semi-novos no site da OLX: https://olx.com.br',
]

# Criando o espaço para armazenar nossos Embeddings
vector = create_emb(d, assuntos)
index.add(vector)

faiss.write_index(index, 'index.bin')


#https://github.com/matsui528/faiss_tips