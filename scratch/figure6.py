import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
import scienceplots
plt.style.use('science')
import os
from matplotlib.ticker import ScalarFormatter
import numpy as np
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np

import subprocess
from multiprocessing import Pool

plt.rcParams['text.usetex'] = False

COLORMAP = {'TcpBbr':  '#00B945',
            'TcpBbr3': '#FF9500'}
LEGENDMAP = {}
BW = 100
DELAY = 20
PRESENTFLOW = 'TcpCubic'
PROTOCOLS = ['TcpBbr', 'TcpBbr3']
RUNS = [1,2,3,4,5]
QMULTS = [0.2, 1, 4]
LINEWIDTH = 1
MODES = ['normal', 'inverse']
EXPERIMENT = 'fairness2flows'
MAX_SIMULATIONS = 32
ENDTIME = 200


# def run_simulation(params):
#     protocol, mult, mult, protocol, run, mode = params
#     if mode == ['inverse']:
#         command = "./ns3 run \"scratch/SimulatorScript.cc --stopTime={} --flowStartOffset=100 --appendFlow={} --appendFlow2={} --queueBDP={} --botLinkDelay={} --path={}-{}/bw{}/delay{}/qmult{}/flows2/{}/run{} --seed={}\"".format(ENDTIME, protocol, PRESENTFLOW, mult, DELAY, EXPERIMENT, mode, BW, DELAY, mult, protocol, run, run)
#     else:
#         command = "./ns3 run --no-build \"scratch/SimulatorScript.cc --stopTime={} --flowStartOffset=100 --appendFlow={} --appendFlow2={} --queueBDP={} --botLinkDelay={} --path={}_{}/bw{}/delay{}/qmult{}/flows2/{}/run{} --seed={}\"".format(ENDTIME, PRESENTFLOW, protocol, mult, DELAY, EXPERIMENT, mode, BW, DELAY, mult, protocol, run, run)
#     subprocess.run(command, shell=True, cwd='../')

# pool = Pool(processes=MAX_SIMULATIONS)

# params_list = [(protocol, mult, mult, protocol, run, mode)
#                for protocol in PROTOCOLS
#                for mult in QMULTS
#                for run in RUNS
#                for mode in MODES]

# pool.map(run_simulation, params_list)

# pool.close()
# pool.join()





for QMULT in QMULTS:
    for mode in MODES:
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(5,2.5), sharex=True)


        if mode == 'inverse':
            ROOT_PATH = "%s_%s" % (EXPERIMENT, mode) 
        else:
            ROOT_PATH = "%s_%s" % (EXPERIMENT, mode) 
        for FLOWS in [2]:
            data = {'flow1':
                        {1: pd.DataFrame([], columns=['time','mean', 'std']),
                        2: pd.DataFrame([], columns=['time','mean', 'std']),
                        3: pd.DataFrame([], columns=['time','mean', 'std']),
                        4: pd.DataFrame([], columns=['time','mean', 'std'])},
                    'flow2':
                        {1: pd.DataFrame([], columns=['time', 'mean', 'std']),
                        2: pd.DataFrame([], columns=['time', 'mean', 'std']),
                        3: pd.DataFrame([], columns=['time', 'mean', 'std']),
                        4: pd.DataFrame([], columns=['time', 'mean', 'std'])}
                    }

            start_time = 0
            end_time = 200
            # Plot throughput over time
            for protocol in PROTOCOLS:
                senders = {1: [], 2: [], 3: [], 4:[]}
                receivers = {1: [], 2: [], 3: [], 4:[]}
                for run in RUNS:
                    PATH = ROOT_PATH + '/bw%s/delay%s/qmult%s/flows2/%s/run%s' % (BW,DELAY,QMULT,protocol,run)
                    for n in range(FLOWS):
                        if mode == 'normal':
                            if n == 0:
                                if os.path.exists(PATH + '/%s%s-goodput.csv' % (PRESENTFLOW, n)):
                                    receiver_total = pd.read_csv(PATH + '/%s%s-goodput.csv' % (PRESENTFLOW, n)).reset_index(drop=True)
                                    receiver_total.columns = ['time', 'bandwidth']
                                    receiver_total['bandwidth'] = receiver_total['bandwidth'].ewm(alpha=0.5).mean()
                                    receiver_total = receiver_total[(receiver_total['time'] >= (start_time)) & (receiver_total['time'] <= (ENDTIME))]
                                    receiver_total = receiver_total.drop_duplicates('time')
                                    receiver_total = receiver_total.set_index('time')
                                    receivers[n+1].append(receiver_total)
                                else:
                                    print("%s not found" % (PATH + '/%s%s-goodput.csv' % (PRESENTFLOW, n)))
                            else:
                                if os.path.exists(PATH + '/%s%s-goodput.csv' % (protocol, n)):
                                    receiver_total = pd.read_csv(PATH + '/%s%s-goodput.csv' % (protocol, n)).reset_index(drop=True)
                                    receiver_total.columns = ['time', 'bandwidth']
                                    #receiver_total = receiver_total[['time', 'bandwidth']]
                                    #receiver_total['time'] = receiver_total['time'].apply(lambda x: int(float(x)))
                                    receiver_total['bandwidth'] = receiver_total['bandwidth'].ewm(alpha=0.5).mean()

                                    receiver_total = receiver_total[(receiver_total['time'] >= (start_time)) & (receiver_total['time'] <= (ENDTIME))]
                                    receiver_total = receiver_total.drop_duplicates('time')
                                    receiver_total = receiver_total.set_index('time')
                                    receivers[n+1].append(receiver_total)
                                else:
                                    print("%s not found" % (PATH + '/%s%s-goodput.csv' % (protocol, n)))
                        else:
                            if n == 1:
                                if os.path.exists(PATH + '/%s%s-goodput.csv' % (PRESENTFLOW, n)):
                                    receiver_total = pd.read_csv(PATH + '/%s%s-goodput.csv' % (PRESENTFLOW, n)).reset_index(drop=True)
                                    receiver_total.columns = ['time', 'bandwidth']
                                    receiver_total['bandwidth'] = receiver_total['bandwidth'].ewm(alpha=0.5).mean()
                                    receiver_total = receiver_total[(receiver_total['time'] >= (start_time)) & (receiver_total['time'] <= (ENDTIME))]
                                    receiver_total = receiver_total.drop_duplicates('time')
                                    receiver_total = receiver_total.set_index('time')
                                    receivers[n+1].append(receiver_total)
                                else:
                                    print("%s not found" % (PATH + '/%s%s-goodput.csv' % (PRESENTFLOW, n)))
                            else:
                                if os.path.exists(PATH + '/%s%s-goodput.csv' % (protocol, n)):
                                    receiver_total = pd.read_csv(PATH + '/%s%s-goodput.csv' % (protocol, n)).reset_index(drop=True)
                                    receiver_total.columns = ['time', 'bandwidth']
                                    #receiver_total = receiver_total[['time', 'bandwidth']]
                                    #receiver_total['time'] = receiver_total['time'].apply(lambda x: int(float(x)))
                                    receiver_total['bandwidth'] = receiver_total['bandwidth'].ewm(alpha=0.5).mean()

                                    receiver_total = receiver_total[(receiver_total['time'] >= (start_time)) & (receiver_total['time'] <= (ENDTIME))]
                                    receiver_total = receiver_total.drop_duplicates('time')
                                    receiver_total = receiver_total.set_index('time')
                                    receivers[n+1].append(receiver_total)
                                else:
                                    print("%s not found" % (PATH + '/%s%s-goodput.csv' % (protocol, n)))
                # For each flow, receivers contains a list of dataframes with a time and bandwidth column. These dataframes SHOULD have
                # exactly the same index. Now I can concatenate and compute mean and std
                for n in range(FLOWS):
                    print(receivers)
                    if len(receivers[n]) > 0:
                        data[protocol][n+1]['mean'] = pd.concat(receivers[n], axis=1).mean(axis=1)
                        data[protocol][n+1]['std'] = pd.concat(receivers[n], axis=1).std(axis=1)
                        data[protocol][n+1].index = pd.concat(receivers[n], axis=1).index

        for i,protocol in enumerate(PROTOCOLS):
            ax = axes[i]

            for n in range(FLOWS):
                if mode == 'inverse':
                    LABEL = protocol if n == 0 else 'cubic'
                    COLOR = '#0C5DA5' if n == 1 else COLORMAP[protocol]
                else:
                    LABEL = protocol if n == 1 else 'cubic'
                    COLOR = '#0C5DA5' if n == 0 else COLORMAP[protocol]

                ax.plot(data[protocol][n+1].index, data[protocol][n+1]['mean'], linewidth=LINEWIDTH, label=LABEL, color=COLOR)
                try:
                    if mode == 'inverse':
                        FC = '#0C5DA5' if n == 1 else COLORMAP[protocol]
                    else:
                        FC = '#0C5DA5' if n == 0 else COLORMAP[protocol]
                    ax.fill_between(data[protocol][n+1].index, data[protocol][n+1]['mean'] - data[protocol][n+1]['std'], data[protocol][n+1]['mean'] + data[protocol][n+1]['std'], alpha=0.2,  fc=FC)
                except:
                    print("Fill between error")


            ax.set(ylim=[0,100])

            ax.grid()

            handles, labels = ax.get_legend_handles_labels()
            for handle, label in zip(handles, labels):
                if not LEGENDMAP.get(label,None):
                    LEGENDMAP[label] = handle

        fig.text(0.5, 0.01, 'time (s)', ha='center')
        fig.text(0.045, 0.5, 'Goodput (Mbps)', va='center', rotation='vertical')


        fig.legend(list(LEGENDMAP.values()), list(LEGENDMAP.keys()), loc='upper center',ncol=3)

        for format in ['pdf']:
            plt.savefig('goodput_friendly_%sms_%s_%s.%s' % (DELAY, QMULT, mode, format), dpi=1080)