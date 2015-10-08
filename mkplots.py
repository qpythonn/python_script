#!/usr/bin/env python

import os,sys
from string import *
from ROOT import *
import time
from array import *

# introduce a boolean that, when set to True, enables various print out
debug=False

# creating output root file
outputFileName= "CF_hist.root"
outputFile = TFile(outputFileName, "RECREATE")
Canvas = TCanvas("")

#print "will exit!!" 
#sys.exit(0)

# Get the ratio of given two histograms
def ratio(hnn, hnd, hne, dh, dhe):
    print hnn, hnd, hne
    h = dh[hnn].Clone()
    h.SetName(hne)
    print "h is ", h 
    print "dh[hnd] is ", [hnd]
    h.Divide(dh[hnd])
    dhe[hne] = h

# Draw 2 efficiencies
def draw2eff(dhe, en, s, si, flavor):

    msf = 1
    efftitle = ''
    if 'b' in flavor:
        efftitle = '#epsilon_{b}'
        msf = 0.1
    if 'c' in flavor:
        efftitle = '#epsilon_{c}'
        msf = 0.2
    if 'l' in flavor:
        efftitle = '#epsilon_{udsg}'
        msf = 0.3

    enFl = 'eff_jet_pt_'+en+'_'+flavor+'_'+si+'_Full'
    enFs = 'eff_jet_pt_'+en+'_'+flavor+'_'+si+'_Fast'
    print enFl, enFs
    hFl = dhe[enFl]
    hFs = dhe[enFs] 

    hFl.SetLineColor(kBlue)
    hFl.SetMarkerColor(kBlue)
    hFl.SetMarkerStyle(20)
    hFl.SetMarkerSize(0.7)
    hFs.SetLineColor(kGreen+2)
    hFs.SetMarkerColor(kGreen+2)    
    hFs.SetMarkerStyle(20)
    hFs.SetMarkerSize(0.7)

    maxi = max(hFl.GetMaximum(), hFs.GetMaximum())*(1.2)
    mini = min(hFl.GetMinimum(), hFs.GetMinimum())*(0.5)
    hFs.SetMaximum(maxi)
    hFs.SetMinimum(mini)


    hFs.SetTitle("")
    hFs.GetXaxis().SetTitle('jet p_{T}')
    hFs.GetXaxis().SetTitleSize(0.055)
    hFs.GetXaxis().SetTitleFont(42)
    hFs.GetXaxis().SetLabelSize(0.050)
    hFs.GetXaxis().SetLabelFont(42)
    hFs.GetYaxis().SetTitle(efftitle)
    #hFs.GetYaxis().SetTitleOffset(0.62)
    hFs.GetYaxis().SetTitleSize(0.055)
    hFs.GetYaxis().SetTitleFont(42)
#    hFs.GetYaxis().SetMaximum(1.2)
    hFs.Draw('pe1')
    hFl.Draw('pe1same')
    hFs.Draw('pe1same')

    # faco

    
    # choose location of the legend a bit more smartly:
    if (flavor == "l"):
        l = TLegend(0.20, 0.75, 0.40, 0.88)    
    else :
        l = TLegend(0.40, 0.15, 0.82, 0.27)    
        

    l.SetBorderSize(0)
    l.SetFillStyle(0000)
    l.SetTextSize(0.045)
    l.SetTextFont(42)
    l.AddEntry(hFl, s[1]+', Full', 'p')
    l.AddEntry(hFs, s[1]+', Fast', 'p')
    l.Draw("same")
    # Make the legend visible (annoying pyROOT-specific feature)
    SetOwnership(l, 0 )

    tex = en[6:]
    if 'For_' in flavor:
        tex = tex + ', |#eta| > 1.2'
    if 'Cen_' in flavor:
        tex = tex + ', |#eta| < 1.2'        
    t = TLatex(0.58, 0.82, tex)
    t.SetNDC()
    t.SetTextSize(0.045)
    t.SetTextFont(42)    
    t.Draw('same')
    SetOwnership(t, 0 )


# Draw 1 CF
def draw1CF(dhcf, en, s, si, flavor):

    msf = 1
    efftitle = ''
    if 'b' in flavor:
        efftitle = 'Full/Fast CF_{b}'
        msf = 0.1
    if 'c' in flavor:
        efftitle = 'Full/Fast CF_{c}'
        msf = 0.2
    if 'l' in flavor:
        efftitle = 'Full/Fast CF_{udsg}'
        msf = 0.3
        
    

    print " samples content is ",     samples[i][0]


    cfn = 'CF_jet_pt_'+en+'_'+flavor+'_'+si # faco
#    print "About to use it!"
#    print "dhcf = ", dhcf
#    print "cfn = ", cfn
    h = dhcf[cfn]

    h.SetLineColor(kRed)
    h.SetMarkerColor(kRed)
    h.SetMarkerStyle(20)
    h.SetMarkerSize(0.7)

    h.SetTitle("")
    h.GetXaxis().SetTitle('jet p_{T}')
    h.GetXaxis().SetTitleSize(0.055)
    h.GetXaxis().SetTitleFont(42)
    h.GetXaxis().SetLabelSize(0.050)
    h.GetXaxis().SetLabelFont(42)
    h.GetYaxis().SetTitle(efftitle)
    #h.GetYaxis().SetTitleOffset(0.62)
    h.GetYaxis().SetTitleSize(0.055)
    h.GetYaxis().SetTitleFont(42)
    # Set range depending on the flavour
    if (flavor == "l" ):
        h.GetYaxis().SetRangeUser(0.5,3)
    elif (flavor == "c" ):
        h.GetYaxis().SetRangeUser(0.5,1.5)
    else :
        h.GetYaxis().SetRangeUser(0.8,1.2)
    h.Draw('pe1')
    
    # Save the histogram in a root file
    outputFile.cd()
    h.Write('CF_jet_pt_'+en+'_'+flavor+'_'+sn)


#    l = TLegend(0.12, 0.15, 0.40, 0.27)
    l = TLegend(0.12, 0.85, 0.40, 0.27)
    l.SetBorderSize(0)
    l.SetFillStyle(0000)
    l.SetTextSize(0.045)
    l.SetTextFont(42)
    l.AddEntry(h, s[1], 'p')
    l.Draw("same")
    # Make the legend visible (annoying pyROOT-specific feature)
    SetOwnership(l, 0 )

    tex = en[6:]
    if 'For_' in flavor:
        tex = tex + ', |#eta| > 1.2'
    if 'Cen_' in flavor:
        tex = tex + ', |#eta| < 1.2'        
    t = TLatex(0.58, 0.82, tex)
    t.SetNDC()
    t.SetTextSize(0.045)
    t.SetTextFont(42)    
    t.Draw('same')
    SetOwnership(t, 0 )


# Draw multi-CFs
def drawnCF(dhcf, en, samples, sn, flavor):

    msf = 1
    efftitle = ''
    if 'b' in flavor:
        efftitle = 'Full/Fast CF_{b}'
        msf = 0.1
    if 'c' in flavor:
        efftitle = 'Full/Fast CF_{c}'
        msf = 0.2
    if 'l' in flavor:
        efftitle = 'Full/Fast CF_{udsg}'
        msf = 0.3

    hs = []
    maxi = 0
    mini = 1000
    for s in sn:
        si = str(s[0])
        cfn = 'CF_jet_pt_'+en+'_'+flavor+'_'+si
        h = dhcf[cfn]
        h.SetLineColor(s[1])
        h.SetMarkerColor(s[1])
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.7)
        if s[0] == 1000:
            h.SetMarkerStyle(24)
        if h.GetMaximum() > maxi: maxi = h.GetMaximum()
        if h.GetMinimum() < mini: mini = h.GetMinimum()
        hs.append(h)

    maxi = maxi*1.1
    mini = mini*0.7
    maxi = 1.2
    mini = 0.3
    if 'c' in flavor: maxi = 1.2
    if 'l' in flavor: maxi = 2.0
#    if 'For_l' in flavor: maxi = 3.0
    

    hs[0].SetMaximum(maxi)
    hs[0].SetMinimum(mini)

    hs[0].SetTitle("")
    hs[0].GetXaxis().SetTitle('jet p_{T}')
    hs[0].GetXaxis().SetTitleSize(0.055)
    hs[0].GetXaxis().SetTitleFont(42)
    hs[0].GetXaxis().SetLabelSize(0.050)
    hs[0].GetXaxis().SetLabelFont(42)
    hs[0].GetYaxis().SetTitle(efftitle)
    #hs[0].GetYaxis().SetTitleOffset(0.62)
    hs[0].GetYaxis().SetTitleSize(0.055)
    hs[0].GetYaxis().SetTitleFont(42)
    hs[0].Draw('pe1')
    for i in range(1,len(hs)):
        hs[i].Draw('pe1same')

    l = TLegend(0.12, 0.15, 0.40, 0.33)
    if len(hs) > 5:
        l = TLegend(0.12, 0.15, 0.40, 0.36)
    l.SetBorderSize(0)
    l.SetFillStyle(0000)
    l.SetTextSize(0.045)
    l.SetTextFont(42)

    for i in range(len(sn)):
        if sn[i][0] != 1000:
            l.AddEntry(hs[i], samples[sn[i][0]][1], 'p')
        else:
            l.AddEntry(hs[i], 'Recipe', 'p')
    l.Draw("same")
    # Make the legend visible (annoying pyROOT-specific feature)
    SetOwnership(l, 0 )

    tex = en
#    if 'For_' in flavor:
#        tex = tex + ', |#eta| > 1.2'
    if 'Cen_' in flavor:
        tex = tex + ', |#eta| < 1.2'        
    t = TLatex(0.58, 0.82, tex)
    t.SetNDC()
    t.SetTextSize(0.045)
    t.SetTextFont(42)    
    t.Draw('same')
    SetOwnership(t, 0 )
 



# Calculate the recipe values for CFs
def mkrcp(dhcf, en, samples, sn, flavor):

    hs = []
    for s in sn:
        si = str(s)
        cfn = 'CF_jet_pt_'+en+'_'+flavor+'_'+si
        h = dhcf[cfn]
        hs.append(h)

    havg = hs[0].Clone()
    cfn = 'CF_jet_pt_'+en+'_'+flavor+'_1000'
    havg.SetName(cfn)
    nbins = hs[0].GetXaxis().GetNbins()
    for b in range(1,nbins+1):
        print b
        abc = array('d')
        aberr = array('d')
        berr2 = 0
        nrms = 0
        for i in range(len(hs)):
            abc.append(hs[i].GetBinContent(b))
            for j in range(i+1, len(hs)):
                err = fabs(hs[i].GetBinContent(b) - hs[j].GetBinContent(b))
                print i, j, err
                aberr.append(err)
                berr2 = berr2 + err*err
                nrms = nrms + 1
        bcavg = TMath.Mean(len(hs), abc)
        berr = sqrt(berr2/nrms)/2.
        berr2 = TMath.RMS(len(hs), abc)
        berr3 = sqrt(float(len(hs))/(float(len(hs)-1)))*TMath.RMS(len(hs), abc)
        print i, j, bcavg, berr, berr2, berr3
        havg.SetBinContent(b, bcavg)
        havg.SetBinError(b, berr3)
        

    dhcf[cfn] = havg


# Sezen's ROOT style:   
gROOT.SetStyle('Plain')
gStyle.SetOptStat(0)
gStyle.SetPalette(1)
    
gStyle.SetTextFont(42)
    
gStyle.SetTitleStyle(0000)
gStyle.SetTitleBorderSize(0)
# More style
gStyle.SetEndErrorSize(2)
gStyle.SetErrorX(0.)


# File names
samples = []
samples.append(['output_TT', 'TTJets'])
samples.append(['output_T1bbbb_mG1000_mLSP900', 'T1bbbb 1000 900'])
samples.append(['output_T1bbbb_mG1500_mLSP100', 'T1bbbb 1500 100'])
"""
samples.append(['output_T1bbbb_mg600_', 'T1bbbb 600 100'])
samples.append(['output_T1bbbb_mg825_', 'T1bbbb 820 200'])
samples.append(['output_T1bbbb_mg1025_', 'T1bbbb 1025 50'])
samples.append(['output_T1bbbb_', 'T1bbbb combined'])
samples.append(['output_T2bb_mb300_', 'T2bb 300 200'])
samples.append(['output_T2bb_mb400_', 'T2bb 400 200'])
samples.append(['output_T2bb_mb600_', 'T2bb 600 50'])
samples.append(['output_T2bb_', 'T2bb combined'])
samples.append(['output_T1tttt_mg600_', 'T1tttt 600 125'])
samples.append(['output_T1tttt_mg825_', 'T1tttt 825 225'])
samples.append(['output_T1tttt_mg1025_', 'T1tttt 1025 75'])
samples.append(['output_T1tttt_', 'T1tttt combined'])
samples.append(['output_T2tt_mt400_', 'T2tt 400 150'])
samples.append(['output_T2tt_', 'T2tt combined'])
"""

# Get the FullSim and FastSim files:
fFl = []
fFs = []
for s in samples:
    fFl.append(TFile(s[0]+'Full.root'))
    fFs.append(TFile(s[0]+'Fast.root'))

# Get the histogram names in an example ROOT file:
histnames = []
rootkeys = fFs[0].GetListOfKeys()
for key in rootkeys:
    histnames.append(key.GetName())

histnames_full = []
rootkeys = fFl[0].GetListOfKeys()
for key in rootkeys:
    histnames_full.append(key.GetName())


if (len(histnames) != len(histnames_full) ):
    "Different number of histograms in FastSim and FullSim root files. Exiting..."
    sys.exit(0)


if (debug):
    # check all histograms one by one
    for i_histo in range(1,len(histnames)):
        if (histnames[i_histo] != histnames_full[i_histo]):
            print "histograms number ", i_histo , "is not the same in FullSim and FastSim! Exiting..."
            sys.exit(0)


print "\n"
print "Comparing number of histos in the different input file"
print "Histnames_fast.size() is ", len(histnames), "and histnames_full.size() is ", len(histnames_full) , "\n\n"


# Names of taggers for which we want an efficiency
effnames = []

"""
# CSVv1
effnames.append('csvl')
effnames.append('csvm')
effnames.append('csvt')
"""

#"""
# CSVv2
effnames.append('csvivfl')
effnames.append('csvivfm')
effnames.append('csvivft')
#"""

#effnames.append('taggedJPL')
#effnames.append('taggedJPM')
#effnames.append('taggedJPT')
#effnames.append('taggedTCHPT')

# Get the histograms
dh = {}
for hn in histnames:
    for i in range(len(fFs)):
        hnFs = hn+'_'+str(i)+'_Fast'
        hnFl = hn+'_'+str(i)+'_Full'
        hFsi = fFs[i].Get(hn)
        if (debug):
            print "hFsi is", hFsi
        hFsi.SetName(hnFs)
        dh[hnFs] = hFsi
        hFli = fFl[i].Get(hn)
        if (debug):
            print "hFli is", hFli
        hFli.SetName(hnFl)
        dh[hnFl] = hFli
        
# Rebin the jet_pt histograms:
jetptbins = [20, 30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670, 800]
ajetptbins = array('d')
ajetptbins.fromlist(jetptbins)
for h in sorted(dh.iterkeys()):
    if 'jet_pt' in h:
        hrb = dh[h].Rebin(16, h, ajetptbins)
        dh[h] = hrb

# Make the efficiency histograms
dhe = {}
for h in sorted(dh.iterkeys()):
    for en in effnames:
        if en in h:
            if "gen" not in h:# temporary fix 
                print "en is ", en
                hnn = h
                print "hnn is ", hnn
                hnd = h.replace(en, "all")
                print "hnd is ", hnd 
                hne = 'eff_'+hnn
                ratio(hnn, hnd, hne, dh, dhe)


# Make the CF histograms
dhcf = {}
for h in sorted(dhe.iterkeys()):
    if '_Full' in h:
        hnn = h
        hnd = h.replace("_Full", "_Fast")
        hne = 'CF_'+hnn[4:-5]
        ratio(hnn, hnd, hne, dhe, dhcf)

flavors = ['b', 'c', 'l']
#flavors = ['b', 'c']
# Make the CF recipe histograms
for flavor in flavors:
    for i in range(len(effnames)):
        en = effnames[i]
        sd = []
        if flavor == 'b':
            sd.append(8)
            sd.append(14)        
            sd.append(4)
            sd.append(12)
            sd.append(0)
        else:
            sd.append(14)
            sd.append(12)
            sd.append(0)
#        mkrcp(dhcf, en, samples, sd, flavor)


# Make tables
def mktable(he, effnames, si, s):

    sn = replace(s[1], ' ', '_')
    fn = 'tables/CF_'+sn+'_'+flavor+'.tex'
    f = open(fn, 'w')

    ncol = len(he)
    cols = '|l|'+ncol*'c|'

    header = '''
\\documentclass[a5paper,10pt]{article}
\\usepackage[landscape,margin=0.15cm]{geometry}
\\usepackage{multirow}
\\begin{document}

\\begin{table}[htbp]
\\fontsize{5 pt}{0.7 em}
\selectfont
%\caption{FullSim and FastSim samples used for obtaining the b tag correction factors.}
\\begin{center}\n'''
    header = header + '''\\begin{tabular}{%(cols)s} \n\hline\n''' % {'cols' : cols}

    titles = 'Bins '
    for en in effnames:
        titles = titles + ' & ' + en
    titles = titles + ' \\\\\n\hline\n'

    footer = '''
\hline
\end{tabular}
\end{center}
\label{default}
\end{table}%
\\end{document} 
    '''

    f.write(header)
    f.write(titles)
    nbins = he[0].GetXaxis().GetNbins()
    for b in range(1,nbins+1):
        line = ''
        binmin = he[0].GetXaxis().GetBinLowEdge(b)
        binmax = he[0].GetXaxis().GetBinUpEdge(b)        
        line = line+str(int(binmin))+'-'+str(int(binmax)) 
        for i in range(len(he)):
            bc = he[i].GetBinContent(b)
            be = he[i].GetBinError(b)
            bval = ' & %.3f $\pm$ %.3f ' % (bc, be)
            line = line + bval
        line = line + '\\\\\n'
        f.write(line)
    f.write(footer)


def mkpayload(he, effnames, si, s):

    fpl = open('fastfull_payload.txt', 'w')

    sn = replace(s[1], ' ', '_')
    fn = 'tables/CF_'+sn+'_'+flavor+'.tex'
    f = open(fn, 'w')

    ncol = len(he)
    cols = '|l|'+ncol*'c|'

    header = '''
\\begin{table}[htbp]
\\fontsize{5 pt}{0.7 em}
\selectfont
%\caption{FullSim and FastSim samples used for obtaining the b tag correction factors.}
\\begin{center}\n'''
    header = header + '''\\begin{tabular}{%(cols)s} \n\hline\n''' % {'cols' : cols}

    titles = 'Bins '
    for en in effnames:
        titles = titles + ' & ' + en
    titles = titles + ' \\\\\n\hline\n'

    footer = '''
\hline
\end{tabular}
\end{center}
\label{default}
\end{table}%
\end{document}   
    '''

    f.write(header)
    f.write(titles)
    nbins = he[0].GetXaxis().GetNbins()
    for b in range(1,nbins+1):
        line = ''
        binmin = he[0].GetXaxis().GetBinLowEdge(b)
        binmax = he[0].GetXaxis().GetBinUpEdge(b)        
        line = line+str(int(binmin))+'-'+str(int(binmax)) 
        for i in range(len(he)):
            bc = he[i].GetBinContent(b)
            be = he[i].GetBinError(b)
            bval = ' & %.3f $\pm$ %.3f ' % (bc, be)
            line = line + bval
        line = line + '\\\\\n'
        f.write(line)
    f.write(footer)


# Write the tables:

write_table=True

if (write_table):
    for flavor in flavors:
        print flavor
        fout = open('btagCF_'+flavor+'.txt', 'w')
        fout.write('float ptmin[] = {')
        for i in range(len(jetptbins)-2):
            fout.write(str(jetptbins[i])+', ')
        fout.write(str(jetptbins[i+1])+'};\n')
        fout.write('float ptmax[] = {')
        for i in range(1,len(jetptbins)-1):
            fout.write(str(jetptbins[i])+', ')
        fout.write(str(jetptbins[i+1])+'};\n\n')
    
        for en in effnames:
            tagger = en
            fout.write('Tagger: '+tagger+' within 20 < pt < 800 GeV, abs(eta) < 2.4\n')
            s = ['Recipe', 'Recipe']
            si = str(0)
            sn = 'average'
            cfn = 'CF_jet_pt_'+en+'_'+flavor+'_'+si
#            cfn = 'CF_jet_pt_'+en+'_'+flavor
            h = dhcf[cfn]
            fout.write('CF_'+flavor+'_'+sn+'[] = {') 
            for b in range(1, h.GetXaxis().GetNbins()):
                fout.write(str(h.GetBinContent(b))+', ')
            fout.write(str(h.GetBinContent(b+1))+'}\n')
            fout.write('CF_'+flavor+'_'+sn+'_err[] = {') 
            for b in range(1, h.GetXaxis().GetNbins()):
                fout.write(str(h.GetBinError(b))+', ')
            fout.write(str(h.GetBinError(b+1))+'}\n')
            for i in range(len(samples)):
                s = samples[i]
                if not ('TTJets' in s[1] or 'combined' in s[1]):
                    continue
                if flavor != 'b':
                    if 'bb' in s[1]:
                        continue
                si = str(i)
                sn = split(s[1])[0]
                cfn = 'CF_jet_pt_'+en+'_'+flavor+'_'+si
                h = dhcf[cfn]
                print "hname: ", h.GetName()
                fout.write('CF_'+flavor+'_'+sn+'[] = {') 
                for b in range(1, h.GetXaxis().GetNbins()):
                    fout.write(str(h.GetBinContent(b))+',')
                fout.write(str(h.GetBinContent(b+1))+'}\n')
                fout.write('CF_'+flavor+'_'+sn+'_err[] = {') 
                for b in range(1, h.GetXaxis().GetNbins()):
                    fout.write(str(h.GetBinError(b))+', ')
                fout.write(str(h.GetBinError(b+1))+'}\n')
            fout.write('\n')
    
#    sys.exit(0)
    
    
    for i in range(len(samples)):
        s = samples[i]
        si = str(i)
        for flavor in flavors:
            he = []
            for en in effnames:
                print en
                cfn = 'CF_jet_pt_'+en+'_'+flavor+'_'+si        
                he.append(dhcf[cfn])
            mktable(he, effnames, si, s)
    
    s = ['Recipe', 'Recipe']
 #   si = str(1000)
    si = str(0)
    for flavor in flavors:
        he = []
        for en in effnames:
            cfn = 'CF_jet_pt_'+en+'_'+flavor+'_'+si        
            he.append(dhcf[cfn])
        mktable(he, effnames, si, s)
    
#    sys.exit()


# Start plotting


bmargin = 0.12
lmargin = 0.12
c = TCanvas('c', 'c', 1000, 1000)
c.Divide(3,2)


for i in range(len(samples)):
    si = str(i)
    s = samples[i]
    sn = s[1].replace(' ', '_')
    for en in effnames:
        c.cd(1)
        c.cd(1).SetBottomMargin(bmargin)
        c.cd(1).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'b')
        c.cd(2)
        c.cd(2).SetBottomMargin(bmargin)
        c.cd(2).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'c')
        c.cd(3)
        c.cd(3).SetBottomMargin(bmargin)
        c.cd(3).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'l')
        c.cd(4)
        c.cd(4).SetBottomMargin(bmargin)
        c.cd(4).SetLeftMargin(bmargin)
        draw1CF(dhcf, en, s, si, 'b')
        c.cd(5)
        c.cd(5).SetBottomMargin(bmargin)
        c.cd(5).SetLeftMargin(bmargin)        
        draw1CF(dhcf, en, s, si, 'c')
        c.cd(6)
        c.cd(6).SetBottomMargin(bmargin)
        c.cd(6).SetLeftMargin(bmargin)
        draw1CF(dhcf, en, s, si, 'l')
        c.Print('plots/p_'+en+'_'+sn+'_bcl.pdf')#faco





bmargin = 0.12
lmargin = 0.12
c = TCanvas('c', 'c', 1000, 1000)
c.Divide(2,2)

for i in range(len(samples)):
    si = str(i)
    s = samples[i]
    sn = s[1].replace(' ', '_')
    for en in effnames:
        c.cd(1)
        c.cd(1).SetBottomMargin(bmargin)
        c.cd(1).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'b')
        c.cd(2)
        c.cd(2).SetBottomMargin(bmargin)
        c.cd(2).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'c')
        c.cd(3)
        c.cd(3).SetBottomMargin(bmargin)
        c.cd(3).SetLeftMargin(bmargin)
#        draw1CF(dhcf, en, s, si, 'b')
        c.cd(4)
        c.cd(4).SetBottomMargin(bmargin)
        c.cd(4).SetLeftMargin(bmargin)        
#        draw1CF(dhcf, en, s, si, 'c')
        c.Print('plots/p_'+en+'_'+sn+'_bc.pdf')#faco

        c.cd(1)
        c.cd(1).SetBottomMargin(bmargin)
        c.cd(1).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'l')
        c.cd(2)
        c.cd(2).SetBottomMargin(bmargin)
        c.cd(2).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'l')
        c.cd(3)
        c.cd(3).SetBottomMargin(bmargin)
        c.cd(3).SetLeftMargin(bmargin)
#        draw1CF(dhcf, en, s, si, 'l')
        c.cd(4)
        c.cd(4).SetBottomMargin(bmargin)
        c.cd(4).SetLeftMargin(bmargin)        
#        draw1CF(dhcf, en, s, si, 'l')
        c.Print('plots/p_'+en+'_'+sn+'_l.pdf')        

        c.cd(1)
        c.cd(1).SetBottomMargin(bmargin)
        c.cd(1).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'b')
        c.cd(2)
        c.cd(2).SetBottomMargin(bmargin)
        c.cd(2).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'c')
        c.cd(3)
        c.cd(3).SetBottomMargin(bmargin)
        c.cd(3).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'l')
        c.cd(4)
        c.cd(4).SetBottomMargin(bmargin)
        c.cd(4).SetLeftMargin(bmargin)
        draw2eff(dhe, en, s, si, 'l')
        c.Print('plots/p_'+en+'_'+sn+'_eff.pdf')        


c1 = TCanvas('c1', 'c1', 1000, 700)
c1.Divide(3,2)


for en in effnames:
    for flavor in flavors:
        c1.cd(1)
        c1.cd(1).SetBottomMargin(bmargin)
        c1.cd(1).SetLeftMargin(bmargin)        
        sd = []
        sd.append([1, kBlue+4])
        sd.append([2, kBlue+2])
        sd.append([3, kBlue])
#        drawnCF(dhcf, en, samples, sd, flavor)

        c1.cd(2)
        c1.cd(2).SetBottomMargin(bmargin)
        c1.cd(2).SetLeftMargin(bmargin)        
        sd = []
        sd.append([5, kGreen+4])
        sd.append([6, kGreen+2])
        sd.append([7, kGreen])
#        drawnCF(dhcf, en, samples, sd, flavor)

        c1.cd(4)
        c1.cd(4).SetBottomMargin(bmargin)
        c1.cd(4).SetLeftMargin(bmargin)        
        sd = []
        sd.append([9, kViolet+4])
        sd.append([10, kViolet+2])
        sd.append([11, kViolet])
#        drawnCF(dhcf, en, samples, sd, flavor)

        c1.cd(5)
        c1.cd(5).SetBottomMargin(bmargin)
        c1.cd(5).SetLeftMargin(bmargin)        
        sd = []
        sd.append([13, kOrange+2])
#        drawnCF(dhcf, en, samples, sd, flavor)

        c1.cd(3)
        c1.cd(3).SetBottomMargin(bmargin)
        c1.cd(3).SetLeftMargin(bmargin)        
        sd = []
        sd.append([0, kRed])
#        drawnCF(dhcf, en, samples, sd, flavor)

        c1.cd(6)
        c1.cd(6).SetBottomMargin(bmargin)
        c1.cd(6).SetLeftMargin(bmargin)        
        sd = []
        sd.append([8, kGreen+1])
        sd.append([14, kOrange+2])        
        sd.append([4, kBlue])
        sd.append([12, kViolet])
        sd.append([0, kRed])
#        drawnCF(dhcf, en, samples, sd, flavor)
        
        c1.Print('plots/p_CF_'+en+'_'+flavor+'.pdf')


#for flavor in flavors:
#    for i in range(len(effnames)):
#        en = effnames[i]
#        c1.cd(i+1)
#        c1.cd(i+1).SetBottomMargin(bmargin)
#        c1.cd(i+1).SetLeftMargin(bmargin)        
#        sd = []
#        sd.append([8, kGreen+1])
#        sd.append([14, kOrange+2])        
#        sd.append([4, kBlue])
#        sd.append([12, kViolet])
#        sd.append([0, kRed])
#        drawnCF(dhcf, en, samples, sd, flavor)
#
#        c1.Print('plots/p_CF_all_'+flavor+'.pdf')


for flavor in flavors:
    for i in range(len(effnames)):
        en = effnames[i]
        c1.cd(i+1)
        c1.cd(i+1).SetBottomMargin(bmargin)
        c1.cd(i+1).SetLeftMargin(bmargin)        
        sd = []
        if flavor == 'b':
            sd.append([8, kGreen+1])
            sd.append([14, kOrange+2])        
            sd.append([4, kBlue])
            sd.append([12, kViolet])
            sd.append([0, kRed])
            sd.append([1000, kBlack])            
        else:
            sd.append([14, kOrange+2])        
            sd.append([12, kViolet])
            sd.append([0, kRed])
            sd.append([1000, kBlack])            
#        drawnCF(dhcf, en, samples, sd, flavor)

        c1.Print('plots/p_CF_all_'+flavor+'.pdf')




outputFile.Close()
