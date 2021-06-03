import pickle
import random
import traceback
import numpy as np
import time
from model import Model
from snake_class import Snake
from utils import clear
from utils import cronometra
import pandas as pd
from tqdm import tqdm

def create_model():
    model2 = Model(1, 20, 20, 20, 4)
    return model2

epoch = 0
# @cronometra
# @cronometra
def crossover(ind1, ind2):
    # NESTE PASSO ESTOU MUTANDO OS PARAMETROS DO IINDIVUO 2 E INDUVIDUO 1 PARA

    mutation = False

    # ESTA FUNCAO FAZ COM QUE O INDIVIDUO TENHA PAREMETROS NAO ALTERADOS TENHA ALGUNS PESOS ORIGINAIS E REALIZO A MUTAÇÃO NOS PESOS DO CRUZAMENTO

    if random.randint(1, 100) <= 3:
        mutation = True # chance to change the individual

    for idx in range(len(ind1)):

        if idx % 2 == 0:
            for hidden in range(len(ind1[idx])):
                cxpoint = random.randint(1, len(ind1[idx][hidden]))
                ind1[idx][hidden][cxpoint:], ind2[idx][hidden][cxpoint:] = ind2[idx][hidden][cxpoint:], \
                                                                           ind1[idx][
                                                                               hidden][
                                                                           cxpoint:]

                if mutation:
                    array_mut1 = np.random.randint(0, 2, size=(len(ind1[idx][hidden]),))
                    ind1[idx][hidden] = np.array(
                        [ind1[idx][hidden][j] * 1.03 if array_mut1[j] == 1 else ind1[idx][hidden][j] * 0.97 for j in
                         range(len(array_mut1))])

                    array_mut2 = np.random.randint(0, 2, size=(len(ind2[idx][hidden]),))
                    ind2[idx][hidden] = np.array(
                        [ind2[idx][hidden][j] * 1.03 if array_mut2[j] == 1 else ind2[idx][hidden][j] * 0.97 for j in
                         range(len(array_mut2))])

        else:
            cxpoint = random.randint(1, len(ind1[idx]))
            ind1[idx][cxpoint:], ind2[idx][cxpoint:] = ind2[idx][cxpoint:], ind1[idx][cxpoint:]

            if mutation:
                array_mut1 = np.random.randint(0, 2, size=(len(ind1[idx]),))
                ind1[idx] = np.array(
                    [ind1[idx][j] * 1.03 if array_mut1[j] == 1 else ind1[idx][j] * 0.97 for j in range(len(array_mut1))])

                array_mut2 = np.random.randint(0, 2, size=(len(ind2[idx]),))
                ind2[idx] = np.array(
                    [ind2[idx][j] * 1.03 if array_mut2[j] == 1 else ind2[idx][j] * 0.97 for j in range(len(array_mut2))])

        model1 = create_model()
        model1.set_weights(ind1)
        model2 = create_model()
        model2.set_weights(ind2)

    return model1, model2


def create_indi(list_indi):
    list_indi_all = []
    prob = pickle.load(open('resources/role.pkl', 'rb'))

    for ind in range(0, 200):
        ind1 = np.random.choice(list_indi, p=prob)
        ind2 = np.random.choice(list_indi, p=prob)
        c, d = crossover(np.array(ind1.get_weights()), np.array(ind2.get_weights()))
        list_indi_all.append(c)
        list_indi_all.append(d)

    return list_indi_all

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Select the mode process [prod, hom, dev, test]')
    parser.add_argument('--version', dest='version', help='version to run')
    args = parser.parse_args()

    list_ind_all = []
    list_ind_score = []
    list_best_ind = []
    list_ind_score_indx = []

    epoch = 0
    population = 400



    try:
        for fator in range(10):
            snake = Snake(args.version+str(fator))
            qtd_ind_gen = int(population / 4)
            for ind in tqdm(range(0, population)):
                list_ind_all.append(create_model())
            for idx, obj in enumerate(list_ind_all):
                snake.rond = [400,
                    80]
                list_ind_score.append(snake.run(obj, epoch))
                list_ind_score_indx.append(idx)
                # INDEX                       #SCORE
            df = pd.DataFrame(list_ind_score_indx, index=list_ind_score)
            df.sort_index(inplace=True)
            bests = df[0].values[-qtd_ind_gen:]

            for id in bests:
                list_best_ind.append(list_ind_all[id])

            path_csv = f'resources/csv/{args.version}.csv'
            file = open(path_csv, 'a+')

            file.write(f'{epoch}, {fator}, {min(list_ind_score)}, {np.mean(list_ind_score)}, {max(list_ind_score)}\n')  # Give your csv text here.
            file.close()

            while True:  # TRAINING EPOCS
                start = time.time()
                epoch += 1
                snake.best_score = 0
                list_ind_all = create_indi(list_best_ind)

                list_ind_score = []
                list_ind_score_indx = []
                list_best_ind = []
                for idx, obj in enumerate(list_ind_all):
                    snake.rond = [400,
                                  80]
                    list_ind_score.append(snake.run(obj, epoch))
                    list_ind_score_indx.append(idx)

                df = pd.DataFrame(list_ind_score_indx, index=list_ind_score)
                df.sort_index(inplace=True)

                file = open(path_csv, 'a+')
                file.write(
                    f'{epoch}, {fator}, {min(list_ind_score)}, {np.mean(list_ind_score)}, {max(list_ind_score)}\n')  # Give your csv text here.
                file.close()
                bests = df[0].values[-qtd_ind_gen:]
                for id in bests:
                    list_best_ind.append(list_ind_all[id])
                end = time.time() - start
                print("This is the time that took for, to finish executing:", end, np.mean(list_ind_score))
                if epoch == 40:
                    break


    except Exception as e:
        formatted_lines = traceback.format_exc().splitlines()
        message = '\n'.join(formatted_lines)
        print(f"LOG[ERROR] {message}")
