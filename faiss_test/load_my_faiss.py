import faiss

index = faiss.read_index("index.bin")  



print("D:", index.d)
print("N:", index.ntotal) 


#print(dir(index))

print(type(index)) #IndexFlatL2


from my_faiss import create_emb

vec = create_emb(4096, ["Consulte o seu saldo"])

index.add(vec)



print("D:", index.d)
print("N:", index.ntotal)


dists, ids = index.search(vec, k=4)

print(ids)

#https://github.com/facebookresearch/faiss/wiki/Faiss-indexes

# import numpy as np
# from my_faiss import search_emb, assuntos, prompt_engenning, make_guess


# # Pergunta a ser respondida
# prompt = 'Eu sofri um acidente de carro, a quem eu devo ligar?'

# # Pesquisa da maior relação entre os embeddings
# relations = search_emb(prompt)
# D, I = index.search(relations, k=len(assuntos))

# # Resposta da pergunta que estava no prompt baseado no embeddings
# assunto_relevante = max(np.array(assuntos)[I.flatten()])
# prompt_enriquecido = prompt_engenning(prompt, assunto_relevante)
# resposta = make_guess(prompt_enriquecido)


# print(resposta)

#https://github.com/matsui528/faiss_tips