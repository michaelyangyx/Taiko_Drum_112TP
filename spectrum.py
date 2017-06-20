import numpy
import wave

"""
Thanks for the following Tutorials for sound processing:
http://blog.csdn.net/xsc_c/article/details/8941338
(in Chinese)
"""

"""
FILE.wav is transformed from mp3 downloaded from iTunes store.
Hall of Fame by the Script
"""

def spectrum(file,difficulty):
    sample=[]
    file=wave.open(file)
    parameters=file.getparams() #get basic parameters of the music file
    nchannels,sampwidth,framerate,nframes=parameters[:4]
    str_data=file.readframes(nframes) #get the frame data
    file.close()
    wave_data=numpy.fromstring(str_data,dtype=numpy.short)
    #transform the frame data to an amplitude array
    wave_data=wave_data.T #use T transformation to get an amplitude list
    time=numpy.arange(0,nframes)*(1.0/framerate)
    #use framerate data to get a list of time
    duration=int(time[-1])+1 #last term in the time list is the actual length
    newSample=intercept(wave_data,duration,sample,difficulty)
    return newSample,duration

def intercept(wave_data,duration,sample,difficulty):
    if difficulty=="Easy": interval,ditch_bound=0.5,5
    elif difficulty=="Medium": interval,ditch_bound=0.4,6
    else: interval,ditch_bound=0.3,8
    newSample=[]
    new_sampling_rate=int(len(wave_data)/(duration/interval))
    #use lower sampling rate (44.1kHz originally)
    for n in xrange(0,len(wave_data),new_sampling_rate):
        sample.append(abs(wave_data[n]))
    maxRate=max(sample)
    for n in sample: #transform from actual amplitudes to the rate amp/maxAmp
        newSample.append(float(n)/maxRate)
    for n in xrange(0,ditch_bound):
        #ditch first 5 amplitudes, beats then go with music
        newSample.pop(0)
        newSample.pop(-1) #avoid additional drums after music over
    return newSample
