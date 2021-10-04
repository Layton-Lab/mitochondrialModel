import numpy as np
import pandas as pd

import pc as pc
import fluxes as fl

J_AtC = 7e-4 ## Used by Edwards et al.
ExpType = 1 ## in vivo = Pyruvate in cytoplasm clamped, cytoplasm has specified water
## volume
StateType = 1 ## Default, remaining Pyruvate concentrations not clamped

o2norm = pc.ics[pc.pcIS.iO2_x]
hleaknorm = pc.params[38]
hcnorm = pc.ics[pc.pcIS.iH_c]
kcnorm = pc.ics[pc.pcIS.iK_c]
mgcnorm = pc.ics[pc.pcIS.iMg_c]

## Conversion factor taken from Edwards et al 2019
rho_m = 1.53e-6
convert = 1e9 * rho_m

def main():
    dictToPD = []

    ## Standard case

    normal = pd.read_csv("../results/resultsATP.csv").tail(1).to_numpy()[0]
    normal = np.delete(normal, [0, 1])
    flVals = fl.fluxes(normal, param=pc.params, ExpType=ExpType, potassiumW=1.0)
    JO2 = (flVals[pc.pcFl.J_C4] / 2.) * convert
    JATP = flVals[pc.pcFl.J_F1] * convert
    PO = JATP / (2. * JO2)
    ATPc = normal[pc.pcIS.iATP_c]
    ADPc = normal[pc.pcIS.iADP_c]
    ARatio = ATPc / ADPc
    pmf = normal[pc.pcIS.idPsi] + ((pc.pcPC.RT * np.log(10)) / pc.pcPC.F) * \
          ((np.log10(normal[pc.pcIS.iH_i])) - (np.log10(normal[pc.pcIS.iH_x])))
    values = {"JO2": JO2, "JATP": JATP, "PO": PO, "PMF": pmf, "ATPc": ATPc * 1000.,
              "ATP/ADP Ratio": ARatio}
    for key in values.keys():
        print(np.round(values[key], 2), end='')
        print(" & ", end='')
    dictToPD.append(values)
    print('\n')

    ## The other cases

    for i in range(19):
        pc.ics[pc.pcIS.iO2_x] = o2norm
        pc.ics[pc.pcIS.iH_c] = hcnorm
        pc.ics[pc.pcIS.iK_c] = kcnorm
        pc.ics[pc.pcIS.iMg_c] = mgcnorm
        pc.params[38] = hleaknorm
        pW = 1.0
        J_AtC = 7e-4

        ## Open files
        mpFile = pd.read_csv("../results/resultsMP"+str(i)+".csv").tail(1).to_numpy()[0]
        mpFile = np.delete(mpFile, [0, 1])

        #print(mpFile[pc.pcIS.idPsi])
        ## Conditions to reproduce (for the altered model) Table 3's observations from Edwards et al
        if i == 0:
            pc.ics[pc.pcIS.iO2_x] = o2norm*(50./23.)
        if i == 1:
            pc.ics[pc.pcIS.iO2_x] = o2norm*0.5
        if i == 2:
            pc.ics[pc.pcIS.iO2_x] = o2norm*(1./3.)
        if i == 3:
            J_AtC = 0.75*J_AtC
        if i == 4:
            J_AtC = 1.25*J_AtC
        if i == 5:
            J_AtC = 1.5*J_AtC
        if i == 6:
            pc.ics[pc.pcIS.iH_c] = 10**-7.4
        if i == 7:
            pc.ics[pc.pcIS.iH_c] = 10**-7.0
        if i == 8:
            pc.ics[pc.pcIS.iH_c] = 10**-6.8
        if i == 9:
            pc.ics[pc.pcIS.iK_c] = 60.0e-3
        if i == 10:
            pc.ics[pc.pcIS.iK_c] = 140.0e-3
        if i == 11:
            pc.ics[pc.pcIS.iMg_c] = 0.2e-3
        if i == 12:
            pc.ics[pc.pcIS.iMg_c] = 0.8e-3
        if i == 13:
            pc.params[38] = 0.0
            pW = 0.0
        if i == 14:
            pc.params[38] = 0.0
        if i == 15:
            pc.params[38] = 0.0
            pW = 10.0
        if i == 16:
            pc.params[38] = hleaknorm*10.0
            pW = 0.0
        if i == 17:
            pc.params[38] = hleaknorm*10.0
        if i == 18:
            pc.params[38] = hleaknorm*10.0
            pW = 10.0

        ## Calculate fluxes
        flVals = fl.fluxes(mpFile, param = pc.params, ExpType = ExpType, potassiumW= pW)

        ## Collecting relevant results
        JO2 = (flVals[pc.pcFl.J_C4]/2.)*convert
        JATP = flVals[pc.pcFl.J_F1]*convert
        PO = JATP/(2.*JO2)
        ATPc = mpFile[pc.pcIS.iATP_c]
        ADPc = mpFile[pc.pcIS.iADP_c]
        ARatio = ATPc/ADPc
        pmf = mpFile[pc.pcIS.idPsi]+((pc.pcPC.RT*np.log(10))/pc.pcPC.F)*\
              ((np.log10(mpFile[pc.pcIS.iH_i])-np.log10(mpFile[pc.pcIS.iH_x])))

        ## Table values
        values = {"JO2": JO2, "JATP": JATP, "PO": PO, "PMF": pmf, "ATPc": ATPc*1000.,
                  "ATP/ADP Ratio": ARatio}
        for key in values.keys():
            print(np.round(values[key], 2), end = '')
            print(" & ", end = '')
        dictToPD.append(values)
        print("\n")

    PD = pd.DataFrame.from_dict(dictToPD, orient = "columns")
    #print(PD)


main()