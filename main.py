import myxgenfile as mgf





if __name__ == '__main__':
    prpath=mgf.judge_pos()
    mgf.createProj(prpath)
    mgf.rewriteKeilconf(prpath)
    mgf.rewritebat(prpath)
    mgf.finishedgen()
    print("[main]Done\n")
    input("Press any key to exit...")

