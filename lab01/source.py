import matplotlib.pyplot as plt
import numpy as np
import math
import scipy
from scipy import signal

EPS = 1e-1

def function1( A, fm, L, t ):
    return A * math.sin( 2* math.pi * ( fm + L ) * t )

def function2( A, fm, L, t ):
    return function1( A, fm, 0, t ) + function1( A, fm, L, t )

def present_graph( X, Y, n, duration, A, message, color ): #graphs n sets of data store in arrays X and Y
    plt.title( message )
    plt.xlabel( 'time(ms)' )
    plt.ylabel( 'Voltage(V)' )

    plt.axis( [ 0, duration, -A, A ] )
    for i in range( 0, n ):
        plt.plot( X[ i ], Y[ i ], color[ i ] )

    plt.show()

def sample_function( fs, n_per, func, *args ): #samples a function func with sampling frequency fs and A = args[ 0 ], fm = args[ 1 ], L = args[ 2 ]
    fm = args[ 1 ]
    T = float( 1.0 / float( fm ) )
    nsamples = n_per * fs / fm
    Y = np.zeros( nsamples ) # we sample over four periods
    X = np.zeros( nsamples )
    time_point = 0
    while( time_point < nsamples ):
        X[ time_point ] = float( time_point ) / fs
        Y[ time_point ] = func( args[ 0 ], args[ 1 ], args[ 2 ], X[ time_point ] )
        time_point = time_point + 1
    return X, Y

def task1( A, fm, L ):
    T = float( 1.0 / float( fm ) )
    #subtask a

    XY1 = np.zeros( ( 2, 80 ) )
    XY2 = np.zeros( ( 2, 400 ) )

    XY1 = sample_function( 20*fm, 4, function1, A, fm, 0 )
    XY2 = sample_function( 100*fm, 4, function1, A, fm, 0 )

    present_graph( [ XY1[ 0 ] ], [ XY1[ 1 ] ], 1, 4*T, A + EPS, 'Sampling of function 1 with sampling frequency: ' + str( 20*fm ) + ' kHz', [ 'bo' ] ) #Graph 1
    present_graph( [ XY2[ 0 ] ], [ XY2[ 1 ] ], 1, 4*T, A + EPS, 'Sampling of function 1 with sampling frequency: ' + str( 100*fm ) + ' kHz', [ 'bo' ] ) #graph 2
    present_graph( [ XY1[ 0 ], XY2[ 0 ] ], [ XY1[ 1 ] - 2*A , XY2[ 1 ] + 2*A ], 2, 4*T, 4*A + EPS,
            'Sampling with both frequencies in mutual axes', [ 'bo', 'ro' ] ) #Graph 3 (Both in mutual axes)

    #subtask b

    XY3 = np.zeros( ( 2, 20 ) )
    XY3 = sample_function( 5*fm, 4, function1, A, fm, L )
    present_graph( [ XY3[ 0 ] ], [ XY3[ 1 ] ], 1, 4*T, A + EPS, 'Sampling of function 1 with sampling frequency: ' + str( 5*fm ) + ' kHz', [ 'bo' ] ) #Sparse Graph

    #subtask c

    XY1 = np.zeros( ( 2, 20 ) )
    XY2 = np.zeros( ( 2, 100 ) )
    XY1 = sample_function( 20*fm, 1, function2, A, fm, L )
    XY2 = sample_function( 100*fm, 1, function2, A, fm, L )

    present_graph( [ XY1[ 0 ] ], [ XY1[ 1 ] ], 1, T, 2*A + EPS, 'Sampling of function 2 with sampling frequency: ' + str( 20*fm ) + ' kHz', [ 'ro' ] ) #Graph 1
    present_graph( [ XY2[ 0 ] ], [ XY2[ 1 ] ], 1, T, 2*A + EPS, 'Sampling of function 2 with sampling frequency: ' + str( 100*fm ) + ' kHz', [ 'ro' ] ) #graph 2
    present_graph( [ XY1[ 0 ], XY2[ 0 ] ], [ XY1[ 1 ] - 4*A , XY2[ 1 ] + 4*A ], 2, T, 8*A + EPS,
            'Sampling with both frequencies in mutual axes', [ 'bo', 'ro' ] ) #Graph 3 (Both in mutual axes)

    XY3 = np.zeros( ( 2, 5 ) )
    XY3 = sample_function( 5*fm, 1, function2, A, fm, L )

    present_graph( [ XY3[ 0 ] ], [ XY3[ 1 ] ], 1, T, 2*A + EPS, 'Sampling of function 1 with sampling frequency: ' + str( 5*fm ) + ' kHz', [ 'ro' ] ) #Sparse Graph

def m( t ): # carrier wave
    return math.sin( 60* math.pi * t )

def AM( A, fm, b, t ):
    ka = 0.5 # ka*Am = 0.5, Am = 1 => ka = 0.5
    return ( 1.0 + ka*m(t) ) * function1( A, fm, 0, t )

def task2( A, fm, R ): #R is the number of bits
    fs1 = 20*fm
    X, Y = sample_function( fs1, 4, function1, A, fm, 0 )
    #subtask 1
    LEVELS = 2 ** R 
    q = 2.0 / ( LEVELS - 1 )
    Y1 = ( np.round( Y / q - 0.5 ) * q + q / 2 )
    plt.title( 'Mid-rise Quantization of the sampled signal with sampling frequency: ' + str(fs1) + 'KHz' )
    plt.xlabel( 'time(ms)' )
    plt.ylabel( 'Binary' )
    Binary = [ str(bin(i))[2:].zfill(4) for i in xrange(0, LEVELS) ]
    Levels_Height = ( np.arange(-1, 1 + q / 2 , q) )
    plt.yticks( Levels_Height  , Binary )
    plt.plot(X, Y, 'bo' )
    plt.step(X, Y1, 'ro' )
    plt.show()
    
    #subtask 2
    s1 = 0
    s2 = 0
    for i in xrange(20):
        if i < 10:
            s1 += ( Y[i] - Y1[i] ) ** 2
        s2 += ( Y[i] - Y1[i] ) ** 2
    s1 = s1 / ( 10 - 1 )
    s2 = s2 / ( 20 - 1 )
    s1 = math.sqrt(s1)
    s2 = math.sqrt(s2)
    print(s1, s2)
    SNR1 = 3 * s1 ** 2 / A * 2 ** (-2 * R)
    SNR2 = 3 * s2 ** 2 / A * 2 ** (-2 * R) 
    print( SNR1, SNR2 )
      
    #subtask 3
    bit_dur = 1 # 1ms
    binary_seq = []
    for i in Y1:
        for j in Binary[ int( i / q + 1 / q  )]:
            binary_seq.append(int(j))
    Y_nrz = np.zeros(len(binary_seq))
    X_nrz = np.zeros(len(binary_seq))
    for i in range(len(binary_seq)):
        Y_nrz[i] = 2 * binary_seq[i] - 1
        X_nrz[i] = i * bit_dur + 1
    plt.title( 'Polar NRZ' )
    plt.xlabel( 'time(ms)' )
    plt.ylabel( 'Voltage(V)' )
    plt.step(X_nrz, Y_nrz, 'bo' ) 
    plt.show()

def task3( A, fm, b ): #b is the modulation factor
    #subtask 1
    T = 1.0 / float( fm )
    XY = np.zeros( ( 2, 400 ) )
    XY = sample_function( 100*fm, 4, AM, A, fm, b )

    present_graph( [ XY[ 0 ] ], [ XY[ 1 ] ], 1, 4*T, 2*A + EPS, 'Sampling AM signal with sampling frequency: ' + str( 100*fm ) + 'kHz', [ 'bo' ] )

    #subtask 2
    print fm + 1
    nyq_rate = 2*fm
    print signal.firwin( fm + 1, fm / nyq_rate )

A = 1
FM = 7
L = 1

def main():
    #task1( A, FM, L )
    task2( A, FM, 4 )
    #task3( A, FM, 0.5 )

if __name__ == "__main__":
    main()
