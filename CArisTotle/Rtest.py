import rpy2.robjects as robjects

from rpy2.robjects.packages import importr

base = importr('base')
utils = importr('utils')
catest = importr('catest')

pi = robjects.r('pi')

o = robjects.r('''
        # create a function `f`
        f <- function(r, verbose=FALSE) {
            if (verbose) {
                cat("I am calling f().\n")
            }
            2 * pi * r
        }
        # call the function `f` with argument value 3
        f(3)
        ''')

r_f = robjects.r['f']

print(pi, o, r_f(3))
