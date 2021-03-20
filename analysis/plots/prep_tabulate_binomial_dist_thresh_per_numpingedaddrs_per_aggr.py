
import sys
import numpy
import scipy
import os
from scipy.stats import binom
import datetime
import collections

bin_size = int(sys.argv[1])

# int_nums = [10, 50, 100, 500, 1000, 5000, 10000]
int_nums = [10000, 50000, 56800, 75000, 100000, 150000, 200000, 250000, 500000, 1000000]
int_durs_to_durlabels = collections.OrderedDict()
int_durs_to_durlabels[3600] = "1_per_h"
int_durs_to_durlabels[3600*4] = "1_per_4h"
int_durs_to_durlabels[3600*6] = "1_per_6h"
int_durs_to_durlabels[3600*8] = "1_per_8h"
int_durs_to_durlabels[3600*12] = "1_per_12h"
int_durs_to_durlabels[86400] = "1_per_d"
int_durs_to_durlabels[7*86400] = "1_per_7d"
int_durs_to_durlabels[30*86400] =  "1_per_30d"

sys.stdout.write("{0:>10}".format("Num_addrs") )    
int_fprobs = []
for dur in int_durs_to_durlabels:

    sys.stdout.write(" & {0:>10}".format(int_durs_to_durlabels[dur]) )
    
    num_660s_bins = dur/float(bin_size)
    int_fprobs.append(1/num_660s_bins)

# print int_fprobs
sys.stdout.write("\\\\\n")

sys.stdout.write("{0:>10}".format("Num_addrs") )
idx = 0
for dur in int_durs_to_durlabels:
    sys.stdout.write(" & {0:.10f}".format(int_fprobs[idx]) )
    idx += 1
sys.stdout.write("\\\\\n")

for int_num in int_nums:
    ls = []
    for int_fprob in int_fprobs:    
    
        # Let's find the minimum number that need to go out, assuming we had been pinging 'num' of these addresses
        # For x upips, how many min failures do we need so that there is a less than 1% probability that they happened independently?
        k = numpy.arange(0,100000)
        binomial_cdf = scipy.stats.binom.cdf(k, int_num, int_fprob)

        min_outs_reqd = 0
        for elem in binomial_cdf:
            if elem > 0.99:
                # print nups, nouts, min_outs_reqd, elem
                break
            min_outs_reqd += 1

        # At this point, the probability of min_outs_reqd or fewer failures is < 1%. Therefore, the minimum number of outages should be *greater* than min_outs_reqd, for there to be l.t. 1% probability that so many failures happened independently
        min_outs_reqd += 1

        outs_cdf = scipy.stats.binom.cdf(min_outs_reqd-1, int_num, int_fprob)
        # op_fp.write("{0} {1} {2} {3}\n".format(us_state, asn, min_outs_reqd, 1 - outs_cdf) )

        ls.append(min_outs_reqd)
        # sys.stderr.write("{0} {1} {2} {3}\n".format(int_num, int_fprob, min_outs_reqd, 1 - outs_cdf) )

    # sys.stdout.write("{0:10} & {1:10} & {2:10} & {3:10} & {4:10}\\\\\n".format(int_num, ls[0], ls[1], ls[2], ls[3]) )
    
    sys.stdout.write("{0:10}".format(int_num) )
    for each_val in ls:
        sys.stdout.write(" & {0:10}".format(each_val) )
    sys.stdout.write("\\\\\n")
