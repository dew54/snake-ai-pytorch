import csv
import numpy as np
from helper import plotOverlapped


def smooth_curve(data_list, window_size=30):
    smoothed_data = []
    for i in range(len(data_list)):
        if i < window_size - 1:
            smoothed_data.append(data_list[i])
        else:
            window_values = data_list[i - window_size + 1:i + 1]
            smoothed_value = sum(window_values) / window_size
            smoothed_data.append(smoothed_value)
    return smoothed_data


# def smoothLoss(data_list):
#     for i, item in enumerate(data_list):
        


def read_csv(file_path):
    dqn_list = []
    exp_dqn_list = []
    ddqn_list = []
    exp_ddqn_list = []

    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        for row in reader:
            dqn_list.append(float(row[0]))
            exp_dqn_list.append(float(row[1]))
            ddqn_list.append(float(row[2]))
            exp_ddqn_list.append(float(row[3]))

    return dqn_list, exp_dqn_list, ddqn_list, exp_ddqn_list


# CSV file paths
scores_csv_file_path = 'scores.csv'
loss_csv_file_path = 'loss.csv'

# Retrieve data from CSV files
dqnScore, expDqnScore, dDqnScore, expdDqnScore = read_csv(scores_csv_file_path)
dqnLoss, expDqnLoss, dDqnLoss, expdDqnLoss = read_csv(loss_csv_file_path)

dqnLoss = smooth_curve(dqnLoss)
expDqnLoss = smooth_curve(expDqnLoss)
dDqnLoss = smooth_curve(dDqnLoss)
expdDqnLoss = smooth_curve(expdDqnLoss)

data = [[dqnScore, expDqnScore, dDqnScore, expdDqnScore], [dqnLoss, expDqnLoss, dDqnLoss, expdDqnLoss]]

plotOverlapped(data, ["Rewards", "Loss"], ["DQN", "DQN-exp", "DDQN", "DDQN-exp"])
