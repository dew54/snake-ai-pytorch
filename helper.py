import matplotlib.pyplot as plt
import datetime
from IPython import display
import re

plt.ion()

# def plotOld(scores, mean_scores):
#     display.clear_output(wait=True)
#     display.display(plt.gcf())
#     plt.clf()
#     plt.title('Training...')
#     plt.xlabel('Number of Games')
#     plt.ylabel('Score')
#     plt.plot(scores)
#     plt.plot(mean_scores)
#     plt.ylim(ymin=0)
#     plt.text(len(scores)-1, scores[-1], str(scores[-1]))
#     plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
#     # plt.show(block=False)
#     name = "score" + str(datetime.datetime.now()) + '.png'
#     plt.savefig('score'+ str(datetime.datetime.now().timestamp()) +'.png')
#     # plt.pause(.1)


def plot(data, labels, color = 'c'):
    num_plots = len(data)
    # plt.clf()
    
    # Create a grid of subplots
    fig, axs = plt.subplots(num_plots, 1, figsize=(8, 6*num_plots))
    
    for i in range(num_plots):
        plt.subplot(num_plots, 1, i + 1)
        plt.title(labels[i])
        plt.xlabel('Number of Games')
        plt.ylabel("Value")
        plt.plot(data[i], color)
        plt.ylim(ymin=0)
        # plt.text(len(data[i]) - 1, data[i][-1], str(data[i][-1]))
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure with a timestamped name
    timestamp = str(datetime.datetime.now())
    timestamp_cleaned = re.sub(r'[^0-9a-zA-Z]+', '_', timestamp)

    # Create the filename
    name = "score"+ timestamp_cleaned+ ".png"
    plt.savefig(name)


def plotOverlapped(data, labels, legends, color = 'c'):
    num_plots = len(data)
    # plt.clf()
    
    # Create a grid of subplots
    fig, axs = plt.subplots(num_plots, 1, figsize=(8, 6*num_plots))
    
    for i in range(num_plots):
        plt.subplot(num_plots, 1, i + 1)
        plt.title(labels[i])
        plt.xlabel('Number of Games')
        plt.ylabel("Value")
        for j, item in enumerate(data[i]):
            plt.plot(item, label=legends[j])
        plt.ylim(ymin=0)
        # if i == 1:
            # plt.ylim(ymax=1)
        plt.legend()

        # plt.text(len(data[i]) - 1, data[i][-1], str(data[i][-1]))
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure with a timestamped name
    timestamp = str(datetime.datetime.now())
    timestamp_cleaned = re.sub(r'[^0-9a-zA-Z]+', '_', timestamp)

    # Create the filename
    name = "score"+ timestamp_cleaned+ ".png"
    plt.savefig(name)


