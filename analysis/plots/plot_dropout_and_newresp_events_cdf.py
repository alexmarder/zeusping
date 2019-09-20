
import sys
import getopt

# Import utils script for inheriting the Jgraph class
dhcp_utils_path = sys.path[0][0:(sys.path[0].find("zeusping") + len("zeusping"))]
sys.path.append(dhcp_utils_path + "/utils")
import jgraph

# For executing commands
import os
import shlex, subprocess
import time

is_talk = 0

class Num_Addrs_CDF(jgraph.CDF_Jgraph):

    def init_jgraph(self, jgr_fname, title=None):
        self.op_fname = jgr_fname
        self.fp = open(self.op_fname, "w")
        # self.fp.write("\nnewgraph clip\n\n")
        self.fp.write("\nnewgraph\n\n") # Not going to clip by default
        self.curvenum = 0
        self.remove_xoffset = False
        self.xlog = False
        self.ylog = False
        if (title != None):
            self.fp.write("\n title : {0}\n\n".format(title))

        # self.sorted_cdf_pts_fnames = []
        self.cdfcolors = [
        # "color 0.8 0.2 0.2",
        # "color 0.2 0.8 0.2",
        # "color 0.2 0.2 0.8",
        # "color 0.7 0.7 0.7",
        # "color 0.2 0.8 0.7",
        # "color 0.7 0.2 0.7",
        # "color 0.7 0.7 0.2",
        # "color 0 0 0",

        # For talk
        "color 0.2 0.8 0.1",
        "color 0.8 0 0",
        "color 0.2 0.2 0.8",
        "color 0.65 0.65 0.2",
        "color 0.1 0.65 0.65",
        "color 0.65 0.3 0.65",
        "color 0.3 0.3 0.3",

        # For paper?
        # "color 0.6 0.9 0.6",
        # "color 0.3 0.6 0.9",
        # "color 0.8 0.2 0.2",
        # "color 0.8 0.8 0.8",
        # "color 0 0 0",

        # Dunno for what...
        # "color 0.2 0.8 0.7",
        # "color 0.4 0.9 0.2",
        # "color 0.9 0 0.9",
        ]
        self.cdflinetypes = [
        "solid",
        "dotted",
        "dotdash",
        # "dotted",
        # "solid",
        "dashed",
        # "longdash",
        # "dotdash",
        # "dotdotdash",
        # "dotdotdashdash",
        # "dotted"
        ]

        
    def config_xaxis(self, xaxis_label):
        conf = '\n'
        conf += 'size 4\n'
        if (self.xlog):
            conf += 'log\n'

        if (is_talk == 1):
            conf += "gray 0.9\n"
            conf += 'label fontsize 16\n'
            conf += 'hash_labels fontsize 14\n\n'
        else:
            pass
            # conf += 'label fontsize 13\n'
            # conf += 'hash_labels fontsize 11\n\n'

        conf += 'label : {0}\n'.format(xaxis_label)
        conf += 'min 0.1\n'

        # conf += 'no_auto_hash_labels\n'
        # conf += 'no_auto_hash_marks\n'
        # # conf += 'hash_at 0.16\n'
        # # conf += 'hash_label at 0.16 : 1mi\n'
        # conf += 'hash_at 1\n'
        # conf += 'hash_label at 1 : 1h\n'
        # if (is_nonperiodic == 1):
        #     conf += 'hash_at 12\n'
        #     conf += 'hash_label at 12 : 12h\n'
        #     conf += 'hash_at 24\n'
        #     conf += 'hash_label at 24 : 1d\n'
        #     conf += 'hash_at 48\n'
        #     conf += 'hash_label at 48 : 2d\n'
        #     conf += 'hash_at 72\n'
        #     conf += 'hash_label at 72 : 3d\n'
        #     conf += 'hash_at 96\n'
        #     conf += 'hash_label at 96 : 4d\n'
        #     conf += 'hash_at 120\n'
        #     conf += 'hash_label at 120 : 5d\n'
        #     conf += 'hash_at 144\n'
        #     conf += 'hash_label at 144 : 6d\n'
        #     conf += 'hash_at 168\n'
        #     conf += 'hash_label at 168 : 1w\n'
        # elif (is_r_vs_n == 1):
        #     conf += 'hash_at 6\n'
        #     conf += 'hash_label at 6 : 6h\n'
        #     conf += 'hash_at 12\n'
        #     conf += 'hash_label at 12 : 12h\n'
        #     conf += 'hash_at 24\n'
        #     conf += 'hash_label at 24 : 1d\n'
        #     # conf += 'hash_at 48\n'
        #     # conf += 'hash_label at 48 : 2d\n'
        #     # conf += 'hash_at 72\n'
        #     # conf += 'hash_label at 72 : 3d\n'
        #     # conf += 'hash_at 168\n'
        #     # conf += 'hash_label at 168 : 1w\n'
        # else:
        #     conf += 'hash_at 6\n'
        #     conf += 'hash_label at 6 : 6h\n'
        #     conf += 'hash_at 12\n'
        #     conf += 'hash_label at 12 : 12h\n'
        #     conf += 'hash_at 24\n'
        #     conf += 'hash_label at 24 : 1d\n'
        #     conf += 'hash_at 72\n'
        #     conf += 'hash_label at 72 : 3d\n'
        #     conf += 'hash_at 168\n'
        #     conf += 'hash_label at 168 : 1w\n'
        #     conf += 'hash_at 336\n'
        #     conf += 'hash_label at 336 : 2w\n'
        #     # conf += 'hash_at 720\n'
        #     # conf += 'hash_label at 720 : 1mo\n'
        #     # conf += 'hash_at 1440\n'
        #     # conf += 'hash_label at 1440 : 2mo\n'
            
        # if ( (is_nonperiodic == 1) ):
        #     # conf += 'min 0 max 169'
        #     conf += 'min 0 max 24'
        # elif (is_r_vs_n == 1):
        #     conf += 'min 0 max 24'
        #     # conf += 'min 1 max 169'
            
        return conf

    
    def config_yaxis(self, yaxis_label):
        conf = '\n'
        if (self.ylog):
            conf += 'log\n'
        if (is_talk == 1):
            conf += "gray 0.9\n"
            conf += 'label fontsize 16\n'
            conf += 'hash_labels fontsize 14\n\n'
        else:
            pass
            # conf += 'label fontsize 13\n'
            # conf += 'hash_labels fontsize 11\n\n'
        conf += 'size 3\n'
        conf += 'label : {0}\n'.format(yaxis_label)
        conf += 'min 0 max 1\n' # TODO: Find out why it goes beyond 1 sometimes
        return conf


    def config_legends(self):
        if (is_talk != 1):
            # if (is_nonperiodic != 1):
            self.fp.write("legend defaults x 200 y 0.2 hjr vjb\n\n")
                # self.fp.write("legend defaults x 1.25 y 0.775 hjl vjc\n\n")
                # self.fp.write("legend defaults x 169 y 0.225 hjr vjc\n\n") # Orange r_vs_n
        else:
            self.fp.write("legend defaults x 1.25 y 0.775 hjl vjc lgray 0.9\n\n")

        i = 0
        j = 0
        k = 0
        
        for cdf_fname in self.cdf_fnames_list:

            sys.stderr.write("Cdf_fname: {0}\n".format(cdf_fname))
            n_vals = self.n_vals[k]

            lab = (cdf_fname.strip().split('_'))[-1]
            
            self.fp.write("newcurve marktype none linethickness 2 linetype {0} {1} label : {2} ({3})\n".format(self.cdflinetypes[j], self.cdfcolors[i], lab, n_vals))
            
            i += 1
            j += 1
            k += 1
            if (j == len(self.cdflinetypes)):
                j = 0
            if (i == len(self.cdfcolors)):
                i = 0


def usage(args):
    sys.stderr.write("usage: {0} -i <inpfiles> -o <opfile> -x <xaxis label> -y <yaxis label>\n".format(args[0]))

if __name__=="__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:x:y:p:t:u", ["inpfile=", "opfile=", "xlabel=", "ylabel=", "path=", "title=", "usage"])
        
    except getopt.GetoptError as err:
        print str(err)
        usage(sys.argv)
        sys.exit(1)

    pathh = './'        
    inpfiles = None
    xlabel = None
    ylabel = None
    title = None

    for o, a in opts:
        if o in ("-i", "--inpfiles"):
            inpfiles = a
        elif o in ("-p", "--path"):
            pathh = a
        elif o in ("-o", "--opfile"):
            op_fname = a
        elif o in ("-x", "--xlabel"):
            xlabel = a
            print xlabel
        elif o in ("-y", "--ylabel"):
            ylabel = a
            print ylabel
        elif o in ("-t", "--title"):
            title = a
            # print title
        elif o in ("-u", "--usage"):
            usage(sys.argv)
            sys.exit(1)
        else:
            assert False, "unhandled option"
                     
    # The input files for the plots are listed in the filename held in the var: inpfiles.
    inp_fnames = []
    inpfiles_fp = open(inpfiles, "r")

    xlabel = "Number of events"
    ylabel = "Cumulative distribution of addresses"

    j = Num_Addrs_CDF()
    if (title == None):
        j.init_jgraph(op_fname)
    else:
        j.init_jgraph(op_fname, title=title)
    # j.set_xlog()
    j.xaxis(xlabel)
    j.yaxis(ylabel)
    dst_fnames = j.copy_cdf_files(pathh, inpfiles_fp)
    j.get_cdf_fnames(dst_fnames)
    j.calc_n_vals_per_fname()
    j.config_legends()
    j.cdf()
    j.exec_jgraph()
    bp_path = "ramapad@bluepill.cs.umd.edu:~/public_html/dhcp_paper/atlas_ripe/asn_analysis/"
    j.scp_to_bp(bp_path)
    # j.cleanup_fnames(dst_fnames)
