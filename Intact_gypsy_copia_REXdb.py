import sys
import re
from collections import OrderedDict

def strPos(strings, x):
    a = re.search(r'\b({})\b'.format(x), strings)
    if a:
        return a.start()

def CheckDomain(strs):
    gypsy_arr = ('GAG', 'PROT', 'RT', 'RH', 'INT')
    copia_arr = ('GAG', 'PROT', 'INT', 'RT', 'RH')
    #gypsy = [strs.find(x) for x in gypsy_arr]
    #copia = [strs.find(x) for x in copia_arr]
    gypsy = [strPos(strs, x) for x in gypsy_arr]
    copia = [strPos(strs, x) for x in copia_arr]
    # check the domains rank
    gypsy_rank = all(gypsy[y] <= gypsy[y+1] for y in xrange(len(gypsy)-1))
    copia_rank = all(copia[y] <= copia[y+1] for y in xrange(len(copia)-1))
    if None in gypsy: gypsy_rank = False
    if None in copia: copia_rank = False
	return gypsy_rank, copia_rank

# parse annotatation
family = OrderedDict()
with open(sys.argv[1]) as f:
    for line in f:
        if line[0] == "#":
            continue
        lsp = line.split()
        chr, source, type, start, end, score, strand, phase, attibutes = lsp
        d_attr = dict([v.split('=') for v in attibutes.strip(';').split(';')])
        Name, Type = [d_attr["Name"], d_attr['Final_Classification']]
        if "gypsy" in Type or "copia" in Type:
            family.setdefault(chr, []).append([Name, strand, Type.replace("Class_I|LTR|", "")])

# find subfamily
subfamily = OrderedDict()
for i in family:
    temp = OrderedDict()
    for j in family[i]:
        N, S, F = j
        temp.setdefault((F, S), []).append(N)
    subfamily[i] = temp

# find intact LTR-RTs
OUT = open(sys.argv[2], 'w')
for i in subfamily:
    if len(subfamily[i]) == 1:
        for j in subfamily[i]:
            subfam, strand = j
            domains = subfamily[i][j]
            if len(set(domains)) >= 5:
                strings = "/".join(domains)
                out_lst = [i, subfam, strings]
                if strand == "+":
                    gypsy_Rank, copia_Rank = CheckDomain(strings)
                    if gypsy_Rank and not copia_Rank:
                        OUT.write("\t".join(out_lst) + "\n")
                    elif copia_Rank and not gypsy_Rank:
                        OUT.write("\t".join(out_lst) + "\n")
                else:
                    strings = "/".join(domains[::-1])
                    gypsy_Rank, copia_Rank = CheckDomain(strings)
                    if gypsy_Rank and not copia_Rank:
                        OUT.write("\t".join(out_lst) + "\n")
                    elif copia_Rank and not gypsy_Rank:
                        OUT.write("\t".join(out_lst) + "\n")
    # nest
    else:
        subfam_lst = []
        strings_lst = []
        for j in subfamily[i]:
            subfam, strand = j
            domains = subfamily[i][j]
            if len(set(domains)) >= 5:
                strings = "/".join(domains)
                if strand == "+":
                    gypsy_Rank, copia_Rank = CheckDomain(strings)
                    if gypsy_Rank or copia_Rank:
                        subfam_lst.append(subfam)
                        strings_lst.append(strings)
                else:
                    strings = "/".join(domains[::-1])
                    gypsy_Rank, copia_Rank = CheckDomain(strings)
                    if gypsy_Rank or copia_Rank:
                        subfam_lst.append(subfam)
                        strings_lst.append(strings)
        if subfam_lst:
            out_lst = [i, ";".join(subfam_lst), ";".join(strings_lst)]
            OUT.write("\t".join(out_lst) + "\n")
OUT.close()
