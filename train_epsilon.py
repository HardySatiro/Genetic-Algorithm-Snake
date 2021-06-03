import random
import traceback

from model_epsilon import ModelEpsilon
from snake_class import Snake
from utils import clear


def create_model():
    model2 = ModelEpsilon(11, 10, 10, 10, 4)
    return model2


# @cronometra
# @cronometra
def crossover(ind1, ind2):
    # NESTE PASSO ESTOU MUTANDO OS PARAMETROS DO IINDIVUO 2 E INDUVIDUO 1 PARA

    # ESTA FUNCAO FAZ COM QUE O INDIVIDUO TENHA PAREMETROS NAO ALTERADOS TENHA ALGUNS PESOS ORIGINAIS E REALIZO A MUTAÇÃO NOS PESOS DO CRUZAMENTO

    for idx in range(len(ind1)):

        if idx % 2 == 0:
            for hidden in range(len(ind1[idx])):
                cxpoint = random.randint(1, len(ind1[idx][hidden]))
                ind1[idx][hidden][cxpoint:], ind2[idx][hidden][cxpoint:] = ind2[idx][hidden][cxpoint:] * 1.05, \
                                                                           ind1[idx][
                                                                               hidden][
                                                                           cxpoint:] * 1.05

                # array_mut1 = np.random.randint(0, 2, size=(len(ind1[idx][hidden]),))
                # ind1[idx][hidden] = np.array(
                #     [ind1[idx][hidden][j] * 1.1 if array_mut1[j] == 1 else ind1[idx][hidden][j] * 0.90 for j in
                #      range(len(array_mut1))])
                #
                # array_mut2 = np.random.randint(0, 2, size=(len(ind2[idx][hidden]),))
                # ind2[idx][hidden] = np.array(
                #     [ind2[idx][hidden][j] * 1.1 if array_mut2[j] == 1 else ind2[idx][hidden][j] * 0.90 for j in
                #      range(len(array_mut2))])

        else:
            cxpoint = random.randint(1, len(ind1[idx]))
            ind1[idx][cxpoint:], ind2[idx][cxpoint:] = ind2[idx][cxpoint:] * 1.05, ind1[idx][cxpoint:] * 1.05

            # array_mut1 = np.random.randint(0, 2, size=(len(ind1[idx]),))
            # ind1[idx] = np.array(
            #     [ind1[idx][j] * 1.1 if array_mut1[j] == 1 else ind1[idx][j] * 0.90 for j in range(len(array_mut1))])
            #
            # array_mut2 = np.random.randint(0, 2, size=(len(ind2[idx]),))
            # ind2[idx] = np.array(
            #     [ind2[idx][j] * 1.1 if array_mut2[j] == 1 else ind2[idx][j] * 0.90 for j in range(len(array_mut2))])

        model1 = create_model()
        # print(len(ind1))
        model1.set_weights(ind1)
        model2 = create_model()
        model2.set_weights(ind2)
        # print(len(ind1[
        # idx]))
    return model1, model2


def create_indi(list_indi):
    list_indi_all = []
    for ind in range(len(list_indi)):
        for ind_mut in range(1, 3):
            if ind + ind_mut >= len(list_indi):
                a, b = crossover(np.array(list_indi[ind].get_weights()),np.array(list_indi[-(ind + ind_mut) + len(list_indi)].get_weights()))
                list_indi_all.append(a)
                list_indi_all.append(b)
            else:
                #
                c, d = crossover(np.array(list_indi[ind].get_weights()),np.array(list_indi[ind + ind_mut].get_weights()))
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

    import pandas as pd

    from tqdm import tqdm

    epoch = 0
    population = 400
    import numpy as np

    clear()
    try:
        snake = Snake(args.version)
        qtd_ind_gen = int(population / 4)
        for ind in tqdm(range(0, population)):
            list_ind_all.append(create_model())
        for idx, obj in enumerate(list_ind_all):
            list_ind_score.append(snake.run(obj, epoch))
            list_ind_score_indx.append(idx)
            # INDEX                       #SCORE
        df = pd.DataFrame(list_ind_score_indx, index=list_ind_score)
        df.sort_index(inplace=True)
        # print(df)

        bests = df[0].values[-qtd_ind_gen:]

        for id in bests:
            list_best_ind.append(list_ind_all[id])

        # list_best_ind = pickle.load(open("bests.pkl", 'rb'))

        while True:  # TRAINING EPOCS
            epoch += 1
            snake.best_score = 0
            # clear()
            list_ind_all = []
            list_ind_all = create_indi(list_best_ind)

            list_ind_score = []
            list_ind_score_indx = []
            list_best_ind = []
            snake.rond = [random.randrange(snake.padding * 2, snake.height_width - snake.padding * 2, snake.padding),
                          random.randrange(snake.padding * 2, snake.height_width - snake.padding * 2, snake.padding)]

            for idx, obj in enumerate(list_ind_all):
                list_ind_score.append(snake.run(obj, epoch))
                list_ind_score_indx.append(idx)

            df = pd.DataFrame(list_ind_score_indx, index=list_ind_score)
            df.sort_index(inplace=True)
            # print(df)
            bests = df[0].values[-qtd_ind_gen:]
            print(df)
            print(bests)
            for id in bests:
                list_best_ind.append(list_ind_all[id])


    except Exception as e:
        formatted_lines = traceback.format_exc().splitlines()
        message = '\n'.join(formatted_lines)
        print(f"LOG[ERROR] {message}")

#     pygame.mixer.music.load("teste.wav")
#     pygame.mixer.music.play(-1)
