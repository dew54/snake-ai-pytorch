import os 
import csv
from agent import *
from ddqn_agent import * 
from helper import plotOverlapped
import numpy as np




if __name__ == '__main__':
    nSteps = 500
    np.random.seed(123)

    # dqnAgent = Agent(None)
    dqnScore, dqnLoss = train(nSteps)
    expDqnScore, expDqnLoss = train(nSteps, "replay")

    dDqnScore, dDqnLoss = trainDdqn(nSteps)
    expdDqnScore, expdDqnLoss = trainDdqn(nSteps, "replay")

    data = [[dqnScore, expDqnScore, dDqnScore, expdDqnScore], [dqnLoss, expDqnLoss, dDqnLoss, expdDqnLoss]]

    plotOverlapped(data, ["Rewards", "Loss"], ["DQN", "DQN-exp", "DDQN", "DDQN-exp"])

    dataScore = zip(dqnScore, expDqnScore, dDqnScore, expdDqnScore)
    dataLoss = zip(dqnLoss, expDqnLoss, dDqnLoss , expdDqnLoss)

    csv_file_path = 'scores.csv'

    # Write data to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['dqn', 'exp-dqn', 'ddqn', 'exp-ddqn'])  # Write header
        for row in dataScore:
            writer.writerow(row)


    csv_file_path = 'loss.csv'

    # Write data to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['dqn', 'exp-dqn', 'ddqn', 'exp-ddqn'])  # Write header
        for row in dataLoss:
            writer.writerow(row)


    # dqnExpAgent = Agent(None)
    # train()





    # data = []
    # dataLoss = []
    # plot_mean_scores, loss = train()
    # data.append(plot_mean_scores)
    # dataLoss.append(loss)
    # exp_plot_mean_scores, exp_loss = train("experience")
    # data.append(plot_mean_scores)
    # dataLoss.append(loss)
    # print("DATALOSS=====", dataLoss)
    # plot(data, ["DQN", "DQN with experience replay"])
    # plot(dataLoss, ["DQN", "DQN with experience replay"], 'orange')

    # save_lists_to_csv([])

    # plot([loss], "loss")
    