import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

list_of_files_to_search = glob.glob("*.txt")
list_of_files_to_search.sort()

def simpleaxis(ax):
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

for each_file in list_of_files_to_search:
	#each_file = 'bba_0_complex.txt'
	aux = ''
	table = []
	with open(each_file, 'r') as f:
		for idx, line in enumerate(f):
		    line_array = line.split()
		    #print(int(idx + 1) % 6 == 3, line_array)
		    if (idx + 1) > 6:
		        if int(idx + 1) % 6 == 1:
		            aux += str(idx+1) + ' '+ str(line_array[3][1:])
		        elif int(idx + 1) % 6 == 3:
		            aux += ' '+ str(line_array[3])
		        elif int(idx + 1) % 6 == 0:
		            aux += ' '+ str(line_array[1])
		            
		            table.append(aux.split())
		            #print(aux)
		            aux = ''

	df = pd.DataFrame(table)
	df.columns = ['row', 'Timestamp', 'Bandwidth', 'BufferOcc']
	df = df.astype(int)
	df['Bandwidth'] = df['Bandwidth']/1000
	

	df['dq'] = df['Bandwidth'] - df['Bandwidth'].shift(+1)
	df['dq'].fillna(0, inplace=True)
	df['dq'] = df['dq'].abs()

	df['dt'] = df['Timestamp'] - df['Timestamp'].shift(+1)
	df['dt'].fillna(0, inplace=True)
	df['dt'] = df['dt'] - 12	
	

	n_rows = df.shape[0]
	QoE = (12*df['Bandwidth'].sum() - df['dq'].sum() - 1000*df.query("dt>=0 and BufferOcc < 12042")['dt'].sum())/(n_rows*2701.125*12)
	
	print(each_file, QoE)	
	'''	
	print(12*df['Bandwidth'].sum())
	print(1000*df.query("dt >= 0 and BufferOcc < 12042")['dt'].sum())
	print(df['dq'].sum())
	print(df)
	break
	'''

#'''
x_axis = [2, 3, 4, 5, 6, 7, 8, 9, 10]
bba_list = [0.9623191982764384, 0.9623191982764384, 0.9623191982764384, 0.9444058126868068, 0.925307362379138, 0.7554345962550879, 0.746015443300741, 0.5122572105831859, 0.3837756240602277]
bola_basic = [0.9804059831037479, 0.9804059831037479, 0.9804059831037479, 0.9804059831037479, 0.9620420885771434, 0.8841791757843402, 0.8290874922045267, 0.614597204133786, 0.14374694847164649]
bola_finite = [0.9804059831037479, 0.9804059831037479, 0.9804059831037479, 0.9804059831037479, 0.9804059831037479, 0.8966666240624314, 0.7695884739383282, 0.5771348592995129, 0.23409730954254065]
buffer_based = [0.918333187156733, 0.918333187156733, 0.918333187156733,
0.9025852161834395, 0.8992347368490643, 0.7595746980792102, 0.7546086161924007, 0.32121262231271946, 0.2505546101822654]

fig_, ax_= plt.subplots(nrows=1, ncols=1,figsize=(12,4))
ax_.plot(x_axis, buffer_based, label = "Simple buffer-based", color='black') #, dashes=[6, 2])
ax_.plot(x_axis, bba_list, label = "BBA", color='blue') #, dashes=[6, 2])
ax_.plot(x_axis, bola_basic, label = "BOLA basic", color='red') #, dashes=[6, 2])
ax_.plot(x_axis, bola_finite, label = "BOLA finite", color='green') #, dashes=[6, 2])
#ax_.set(xlabel='Packet loss rate (%)', ylabel='QoE')
plt.xlabel('Packet loss rate (%)', fontsize=12)
plt.ylabel('QoE', fontsize=12)
ax_.legend(fontsize = 'large', frameon=False)
plt.savefig('LossVsQoE.pdf', bbox_inches='tight')
plt.show()
#'''




fig, ax = plt.subplots(nrows=3, ncols=1,figsize=(12,12)) #, sharex=True)

network = [1, 1, 1, 1, 1, 1,
	   2, 2, 2, 2, 2, 
           3, 3, 3, 3, 3,
	   4, 4, 4, 4, 4,
           5, 5, 5, 5, 5,
           1, 1, 1, 1, 1,
           2, 2, 2, 2, 2,
           3, 3, 3, 3, 3, 3]
ax[0].plot(range(1, n_rows*12+1, 12), network, label = "Simulated Network") #, color='black')

for each_complex in ['buffer_complex.txt', 'bba_0_complex.txt', 'bola_basic_complex.txt', 'bola_finite_complex.txt']:
	aux = ''
	table = []
	with open(each_complex, 'r') as f:
		for idx, line in enumerate(f):
		    line_array = line.split()
		    #print(int(idx + 1) % 6 == 3, line_array)
		    if (idx + 1) > 6:
		        if int(idx + 1) % 6 == 1:
		            aux += str(idx+1) + ' '+ str(line_array[3][1:])
		        elif int(idx + 1) % 6 == 3:
		            aux += ' '+ str(line_array[3])
		        elif int(idx + 1) % 6 == 0:
		            aux += ' '+ str(line_array[1])
		            
		            table.append(aux.split())
		            #print(aux)
		            aux = ''

	df = pd.DataFrame(table)
	df.columns = ['row', 'Timestamp', 'Bandwidth', 'BufferOcc']
	df = df.astype(int)
	df['Bandwidth'] = df['Bandwidth']/1000
	n_rows = df.shape[0]


	if each_complex == 'buffer_complex.txt':
		ax[1].plot(range(1, n_rows*12+1, 12), df['Bandwidth'], 'black', label = "Simple buffer-based")
		ax[2].plot(range(1, n_rows*12+1, 12), df['BufferOcc'], 'black', label = "Simple buffer-based")
	elif each_complex == 'bba_0_complex.txt':
		ax[1].plot(range(1, n_rows*12+1, 12), df['Bandwidth'], 'blue', label = "BBA")
		ax[2].plot(range(1, n_rows*12+1, 12), df['BufferOcc'], 'blue', label = "BBA")
	elif each_complex == 'bola_basic_complex.txt':
		ax[1].plot(range(1, n_rows*12+1, 12), df['Bandwidth'], 'red', label = "BOLA basic")
		ax[2].plot(range(1, n_rows*12+1, 12), df['BufferOcc'], 'red', label = "BOLA basic")
	elif each_complex == 'bola_finite_complex.txt':
		ax[1].plot(range(1, n_rows*12+1, 12), df['Bandwidth'], 'green', label = "BOLA finite")
		ax[2].plot(range(1, n_rows*12+1, 12), df['BufferOcc'], 'green', label = "BOLA finite")


	
#ax[0].set(xlabel='Time(s)', ylabel='Bandwidth throttling (Mbps)')
#ax[1].set(xlabel='Time(s)', ylabel='Bitrate (kbps)')
#ax[2].set(xlabel='Time(s)', ylabel='Buffer ocupancy (ms)')
ax[0].set_xlabel('Time(s)', fontsize = 12)
ax[0].set_ylabel('Bandwidth throttling (Mbps)', fontsize = 12)
ax[1].set_xlabel('Time(s)', fontsize = 12)
ax[1].set_ylabel('Bitrate (kbps)', fontsize = 12)
ax[2].set_xlabel('Time(s)', fontsize = 12)
ax[2].set_ylabel('Buffer ocupancy (ms)', fontsize = 12)



simpleaxis(ax[0])
simpleaxis(ax[1])
simpleaxis(ax[2])

for ax in fig.get_axes():
    ax.label_outer()
fig.subplots_adjust(hspace=0.2)
ax.legend(bbox_to_anchor=(0.50,1.1), loc="upper center", ncol=4, frameon=False)
#ax.legend(bbox_to_anchor=(0.50,1.1), loc="upper center", ncol=4, frameon=False)

#ax[0].xaxis.set_ticks_position('bottom') #spines('right').set_visible(False)
#ax[0].xaxis.set_ticks_position('left') #spines('right').set_visible(False)
#ax[2].xaxis.set_ticks_position('bottom') #spines('right').set_visible(False)

plt.savefig('Bandwidth_throttling.pdf', bbox_inches='tight')
plt.show()
