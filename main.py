import myxgenfile as mgf
import os
import sys





if __name__ == '__main__':
    prpath=mgf.judge_pos()
    mgf.createProj(prpath)
    mgf.rewriteKeilconf(prpath)
    mgf.rewritebat()
    mgf.finishedgen()
    print("[main]Done\n")