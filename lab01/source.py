import matplotlib.pyplot as plt
import numpy as np
import math
import scipy

EPS = 1e-1

def function1( A, fm, t ):
    return A * math.sin( 2* math.pi * fm * t )

def function2( A, fm, t, L ):
    return function1( A, fm, t ) + A * math.sin( 2 * math.pi * ( fm + L ) * t )

def sample_function1( A, fm, fs ):
    T = float( 1.0 / float( fm ) )
    nsamples = 4 * fs / fm
    Y = np.zeros( nsamples ) # we sample over four periods
    X = np.zeros( nsamples )
    time_point = 0
    while( time_point < nsamples ):
        X[ time_point ] = float( time_point ) / fs
        Y[ time_point ] = function1( A, fm, X[ time_point ] )
        time_point = time_point + 1
    plt.plot( X, Y, 'bo' )

def sample_function2( A, fm, fs, L ):
    T = float( 1.0 / float( fm ) )
    nsamples = 4 * fs / fm
    Y = np.zeros( nsamples ) # we sample over four periods
    X = np.zeros( nsamples )
    time_point = 0
    while( time_point < nsamples ):
        X[ time_point ] = float( time_point ) / fs
        Y[ time_point ] = function2( A, fm, X[ time_point ], L )
        time_point = time_point + 1
    plt.plot( X, Y, 'ro' )

def task1( A, fm, L ):
    #subtask a
    T = float( 1.0 / float( fm ) )
    sample_function1( A, fm, 20*fm )
    sample_function1( A, fm, 100*fm )

    plt.axis( [ 0, 4*T, -( A + EPS ), ( A + EPS ) ] )
    plt.show()

    #subtask b

    sample_function1( A, fm, 5*fm )

    #subtask c
    sample_function2( A, fm, 20*fm, L )
    sample_function2( A, fm, 100*fm, L )

    plt.axis( [ 0, 4*T, -( 2*A + EPS ), ( 2*A + EPS ) ] )
    plt.show()

    sample_function2( A, fm, 5*fm, L )

def task3():

def main():
    task1( 1, 7, 1 )

if __name__ == "__main__":
    main()
