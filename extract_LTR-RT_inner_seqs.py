import sys
from collections import OrderedDict

USAGE = "\nusage: python  %s genome.fasta azfi_ltrdigest_tabout.csv out.fasta\n" % sys.argv[0]

if len(sys.argv) != 4:
    print USAGE
    sys.exit()

def parseFasta(filename):
    fas = {}
    id = None
    with open(filename, 'r') as fh:
        for line in fh:
            if line[0] == '>':
                header = line[1:].rstrip()
                id = header.split()[0]
                fas[id] = []
            else:
                fas[id].append(line.rstrip())
        for id, seq in fas.iteritems():
            fas[id] = ''.join(seq)
    return fas

def coortoDict(filename):
    coor = OrderedDict()
    with open(filename, 'r') as f:
        for line in f:
            lsp = line.split("\t")
            if lsp[0] == "element start": continue
            chr, LTR_start, LTR_end, lLTR_end, rLTR_start = lsp[3], lsp[0], lsp[1], int(lsp[5]) + 1, int(lsp[7]) - 1
            if rLTR_start > lLTR_end:
                id = "_".join([chr, LTR_start, LTR_end])
                coor.setdefault(chr, []).append([lLTR_end, rLTR_start, id])
    return coor

fas_dict = parseFasta(sys.argv[1])
coors = coortoDict(sys.argv[2])
OUT = open(sys.argv[3], 'w')

for i in coors:
    for j in coors[i]:
        id = j[2]
        seq = fas_dict[i][j[0]-1: j[1]]
        OUT.write(">" + id  + "\n" + seq + "\n")
OUT.close()
