import json
import math

import numpy as np
import time


#Carrega dados do arquivo coleção
def load_data_file(path):
    tweets = {}
    with open(path) as fileobject:
        for line in fileobject:
            json_line = json.loads(line)
            tweets[json_line["data"]["id"]] = json_line
    return tweets

#Constroi uma lista de usuários contendo o id e o nome do usuário em cada entrada da lista e também uma ultima posição que será utilizada na "make_matriz" para construir o número de referências feitas a cada usuário
#Retorna a lista construída e também um dicionário que mapeia cada id de usuário ao índice da lista.
def get_users_list(data_obj):
    map_users = {}
    list_users = []
    count = 0
    for key in data_obj:
        user = data_obj[key]["data"]["author_id"]
        username = data_obj[key]["includes"]["users"][0]["username"]
        if user not in map_users:
            map_users[user] = count
            list_users.append([user, username, 0])
            count += 1
    return map_users, list_users

#Estrutura a matriz e organiza os dados para serem extraídas informações posteriormente.
def make_matrix(tweets):
    users_dict, list_users = get_users_list(tweets)
    matrix = np.zeros((len(users_dict), len(users_dict)))
    for key in tweets:
        tweet = tweets[key]
        author = tweet["data"]["author_id"]
        author_index = users_dict[author]
        if "referenced_tweets" in tweet["data"]:
            for ref in tweet["data"]["referenced_tweets"]:
                if ref["id"] in tweets:
                    ref_tweet = tweets[ref["id"]]
                    ref_author = ref_tweet["data"]["author_id"]
                    ref_author_index = users_dict[ref_author]
                    matrix[author_index, ref_author_index] = matrix[author_index, ref_author_index] + 1
                    list_users[ref_author_index][2] += 1
    sums = matrix.sum(axis=1, keepdims=True)
    return list_users, np.divide(matrix, sums, np.zeros_like(matrix), where=sums != 0)


def page_rank(data_matrix, tolerance, beta):
    others = np.ones(data_matrix.shape) * (1 - beta) / data_matrix.shape[1]
    w_data_matrix = data_matrix * beta
    diff = math.inf
    vector = np.ones(data_matrix.shape[0])
    while diff > tolerance:
        nv = np.dot(w_data_matrix + others, vector)
        diff = abs(np.sum(nv - vector))
        vector = nv
    return vector


start_time = time.time()

data_obj = load_data_file("twitter_filtered.txt")

load_data_time = time.time()

users, m = make_matrix(data_obj)

make_matrix_time = time.time()

v = page_rank(m, 0.1, 0.8)

page_rank_time = time.time()



sorted_users = [x for _, x in sorted(zip(v, users))]

sorted_names = [x[1] for x in sorted_users]

sorted_references_made = [x[2] for x in sorted_users]

number_tweets = np.zeros(len(sorted_users))

user_tweets = [[] for _ in range(len(sorted_users))]

for userindex in range(0, len(sorted_users)):
    for el in data_obj.values():
        if el["data"]["author_id"] == sorted_users[userindex][0]:
            user_tweets[userindex].append(el["data"]["text"])
            number_tweets[userindex] = number_tweets[userindex] + 1

n = 20

print("Tempo de carregamento dos dados (em segundos):")
print(load_data_time - start_time)

print("Tempo de construção da matriz (em segundos):")
print(make_matrix_time - load_data_time)

print("Tempo de realização do Page-Rank (em segundos)")
print(page_rank_time - make_matrix_time)

print("Número de usuários")
print(len(sorted_users))
print("Número total de tweets")
print(len(data_obj))
print("\n")

#Dados dos n primeiros.
print(f"--> Nomes dos {n} primeiros")
print(sorted_names[:n])
print(f"--> Números de tweets dos {n} primeiros")
print(number_tweets[:n])
print(f"--> Textos de tweets dos {n} primeiros")
print(user_tweets[:n])
print(f"--> Número de referências ao usuário, para os {n} primeiros")
print(sorted_references_made[:n])
print("\n")

#Dados dos n últimos.
print(f"--> Nomes dos {n} ultimos")
print(sorted_names[-n:])
print(f"--> Números de tweets dos {n} ultimos")
print(number_tweets[-n:])
print(f"--> Textos de tweets dos {n} ultimos")
print(user_tweets[-n:])
print(f"--> Número de referências ao usuário, para os {n} últimos")
print(sorted_references_made[-n:])
