# SAMPLE Output from ThermoCalc computer

> Input on remote machine: `python tc.py "{""Ru"":15, ""Nb"":70, ""Ti"":15}`

> Note: I think the annoying double quote thing on the dictionary keys is necessary to pass the info properly on windows.

13:48:25,439 [Thread-1] INFO  CalculationEngine: Starting Thermo-Calc 2024a, Java-version: 21
13:48:28,658 [Thread-1] INFO  CalculationEngine: Opening database::TCHEA7::
13:48:32,079 [Thread-1] INFO  JavaWrapper: *** Invoking Gibbs Energy System v6 ***
13:48:32,260 [Thread-1] INFO  CalculationEngine:  Creating a new composition set BCC_B2#2
13:48:32,260 [Thread-1] INFO  CalculationEngine: New CS: BCC_B2#2
13:48:32,260 [Thread-1] INFO  CalculationEngine: New CS: BCC_A2#2
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'SSUB6 (2017): SGTE Substance Database V6.0, provided by TCSAB'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'N. Dupin, fixing VA:VA=30*T'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Default volume data, V0DFLT=7.0E-6; VADFLT=10.0E-6*THREE*DELTAT'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'A.T. Dinsdale, SGTE Data for Pure Elements, NPL Report DMA(A) 195 Rev.
13:48:39,573 [Thread-1] INFO  CalculationEngine:        August 1990'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'N. Dupin, introduction of Nb to NI15VA-4SL'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'X.-G. Lu, M. Selleby and B. Sundman, CALPHAD, Vol. 29, 2005, pp. 68-89;
13:48:39,573 [Thread-1] INFO  CalculationEngine:        Molar volumes'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'A. Markstrom, Swerea KIMAB, Sweden; Molar volumes'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Volume data for TCFE4, 2006'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'N. Saunders, COST 507 Report (1998); Al-Nb'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'J.M. Joubert, B. Sundman, N. Dupin, Calphad, 28 (3) 299-306 2004'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Volume data, N. Dupin 2008'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'G(LAVES,AA)=3*G(SER,AA)+15000'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Thermo-Calc Software AB, Stockholm, 2019; Molar volumes'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'J. Bratberg, Thermocalc Software AB, Stockholm, Sweden, 2010'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'S. Liu et al., CALPHAD 38 (2012) 43-58'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'New sigma using combined CEF'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'S. Prince, B. Sundman, Al-Ru'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'X.-G Lu, PhD thesis work'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'N. Dupin, AD/SN, Ru-W'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Alan Dinsdale, SGTE Data for Pure Elements, Calphad Vol 15(1991) p 317
13:48:39,573 [Thread-1] INFO  CalculationEngine:        -425, also in NPL Report DMA(A)195 Rev. August 1990'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'C. Wang et al. JPED 35 (2014) 269-275; Ir-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'L. Kjellqvist, TCSAB, Stockholm, 2012; Molar volumes'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'COST 507, 2nd round'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'J. De Keyzer, G. Cacciamani, N. Dupin, P. Wollants, Fe-Ni-Ti, Calphad 2008'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'A. Markstrom, Thermo-Calc Software AB (2015)'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Thermo-Calc Software AB, Sweden, 2019; re-model and merge
13:48:39,573 [Thread-1] INFO  CalculationEngine:        NI3SN_D019 into ALTI3_D019. '
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'N. Dupin, Thesis, LTPCM, France, 1995; Al-Ni-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'N. Dupin, August 1999, unpublished revision; Cr-Ni-Ti, Al-Cr-Ni-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'J. Bratberg, Thermocalc Software AB, Stockholm, Sweden, 2009'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'A. Markstrom, Thermo-Calc Software AB (2015) Al-Cr-Ni-Ta-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'V.T. Witusiewicz, J. Alloys Compd. 465 (2008) 64-77. Al-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Yang YANG, Molar volume of Ti-Al for project Ti/TiAl II, 2017'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H L Chen, Pure elements
13:48:39,573 [Thread-1] INFO  CalculationEngine:         solid solutions of Omega, TCTI, 2015-16'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'L Kjellqvist, Thermo-Calc Software AB, Stockholm, 2010; UN_ASSessed
13:48:39,573 [Thread-1] INFO  CalculationEngine:        parameter, linear combination of unary volume data'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'P. Canale, Z. Metallkd., 93(4)(2002)273-76,Cu-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'L. Kjellqvist, Thermo-Calc Software AB, Stockholm, 2010; Unassessed
13:48:39,573 [Thread-1] INFO  CalculationEngine:        parameter, linear combination of unary volume data'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, TCSAB, 2022; reassessment of Ir-Nb'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Thermo-Calc Software AB, Sweden, 2013; Unpublished assessment of
13:48:39,573 [Thread-1] INFO  CalculationEngine:        Mn-Ru. '
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Thermo-Calc Software AB, Stockholm, 2013; Molar volumes'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Liangyan Hao, TCS inc, 2022; Rh-X binary (X = Nb, Si, Ta, V, Y)'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H.L. Chen, database editing,in TCNI Project'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Same or similar interaction as in the corresponding stable phase'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H L Chen, Remodeling of Nb-Sn for the Ti/TiAl project, 2017'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'B.J. Lee, Met Mat. Trans. A, 32A, 2423-2439, 2001; C-Fe-N-Nb-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Checking all ternary assessed with ternary module; January 2009'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Unassessed PARAMETER, linear combination of unary data (MU,SIGMA)'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H.L. Chen, modifications and refinements, (2015)'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Y. Gao, C. Guo, et al. J. Alloys Compd. 479 (2009) 148-151. revised by
13:48:39,573 [Thread-1] INFO  CalculationEngine:        Hai-Lin Chen on 2012-04; Ru-Ti'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H L Chen, Assessments
13:48:39,573 [Thread-1] INFO  CalculationEngine:         refinements for the Ti/TiAl project, 2016'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Yang YANG, Molar volume of Ti-Co for project Ti/TiAl II, 2017'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'V.T. Witusiewicz, J Alloys Compd, 472 (2009) 133-161; Al-Nb-Ti Modified
13:48:39,573 [Thread-1] INFO  CalculationEngine:        by Hai-Lin Chen (2016)'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Thermo-Calc Software AB, Sweden, 2019; update of Nb-Ti and Al-Nb
13:48:39,573 [Thread-1] INFO  CalculationEngine:        -Ti. '
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'C. Toffolon, N. Dupin; Fe-Nb-Zr'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Thermo-Calc Software AB, Stockholm, 2017; Modification of the
13:48:39,573 [Thread-1] INFO  CalculationEngine:        HEUSLER_L21 phase according to the validation in multi-component
13:48:39,573 [Thread-1] INFO  CalculationEngine:        systems, Al-Co-Cr-Fe-Hf-Nb-Ni-Ru-Ta-Ti-Zr'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'M Ghasemi, Thermo-Calc Software AB (2019): assessing the viscosity of
13:48:39,573 [Thread-1] INFO  CalculationEngine:        metallic liquid'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'T Ishikawa, Meas Sci Technol 23 (2012) 025305; Ti, Ni, Zr, Nb, Ru, Rh, Hf,
13:48:39,573 [Thread-1] INFO  CalculationEngine:         Ir, Pt, Tb'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'M Ghasemi, Thermo-Calc Software AB (2021): assessing the viscosity of
13:48:39,573 [Thread-1] INFO  CalculationEngine:        metallic liquid'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Y.Tang, in TCCU2, Thermocalc Software AB, Stockholm, Sweden'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'M. Ghasemi, Thermo-Calc Software: Unifying liquid volume database, 2020'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'M Ghasemi, Thermo-Calc Software AB: assessing the surface tension of
13:48:39,573 [Thread-1] INFO  CalculationEngine:        metallic liquid, 2020'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'R. Zhang, Thermo-Calc Software AB, Sweden 2023; Reassessment of surface
13:48:39,573 [Thread-1] INFO  CalculationEngine:        tension using RK rule'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H-L Chen, in TCAL7.0, Evaluation and modeling of electrical resistivity
13:48:39,573 [Thread-1] INFO  CalculationEngine:         thermal conductivity'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'R. Naraghi, Thermo-Calc Software AB, Sweden, 2021; Default values for
13:48:39,573 [Thread-1] INFO  CalculationEngine:        ELRS/THCD'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H-L Chen, Default value for thermal conductivity'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H-L Chen, Default value for electrical resistivity'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Estimation of ELRS
13:48:39,573 [Thread-1] INFO  CalculationEngine:         THCD, Thermo-Calc Software. '
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'H. Mao, Assessment of ELRS
13:48:39,573 [Thread-1] INFO  CalculationEngine:         THCD, Thermo-Calc Software. '
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'Yang YANG, Thermo-Calc Software AB, Sweden, 2021; Assessment of ELRS/THCD
13:48:39,573 [Thread-1] INFO  CalculationEngine:        for Ti alloys'
13:48:39,573 [Thread-1] INFO  CalculationEngine:    'M Ghasemi, Thermo-Calc Software, 2020: ELRS/THCD of liquid'
13:48:44,921 [Thread-1] INFO  CalculationEngine:  Creating a new composition set BCC_B2#3
13:48:44,921 [Thread-1] INFO  CalculationEngine: New CS: BCC_B2#3
13:48:44,921 [Thread-1] INFO  CalculationEngine: New CS: BCC_A2#3
373.15
773.15
1073.15
1173.15
1273.15
1373.15
1423.15
1473.15
1523.15
1573.15
1623.15
1673.15
1723.15
1773.15
1823.15
1873.15
1923.15
1973.15
2023.15
2073.15
2123.15
2173.15
2223.15
2273.15
                Global Composition  Temperature  ... IsOrdered  LatticeParameter
0   {'Ru': 15, 'Nb': 70, 'Ti': 15}       373.15  ...       0.0          3.302327
1   {'Ru': 15, 'Nb': 70, 'Ti': 15}       373.15  ...       1.0          3.154783
2   {'Ru': 15, 'Nb': 70, 'Ti': 15}       773.15  ...       0.0          3.311933
3   {'Ru': 15, 'Nb': 70, 'Ti': 15}       773.15  ...       1.0          3.166502
4   {'Ru': 15, 'Nb': 70, 'Ti': 15}      1073.15  ...       0.0          3.316898
5   {'Ru': 15, 'Nb': 70, 'Ti': 15}      1073.15  ...       1.0          3.181538
6   {'Ru': 15, 'Nb': 70, 'Ti': 15}      1173.15  ...       0.0          3.317605
7   {'Ru': 15, 'Nb': 70, 'Ti': 15}      1173.15  ...       1.0          3.187072
8   {'Ru': 15, 'Nb': 70, 'Ti': 15}      1273.15  ...       0.0          3.317546
9   {'Ru': 15, 'Nb': 70, 'Ti': 15}      1273.15  ...       1.0          3.192517
10  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1373.15  ...       0.0          3.316555
11  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1373.15  ...       1.0          3.197773
12  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1423.15  ...       0.0          3.315667
13  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1423.15  ...       1.0          3.200330
14  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1473.15  ...       0.0          3.314497
15  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1473.15  ...       1.0          3.202853
16  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1523.15  ...       0.0          3.313031
17  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1523.15  ...       1.0          3.205352
18  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1573.15  ...       0.0          3.311262
19  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1573.15  ...       1.0          3.207840
20  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1623.15  ...       0.0          3.309189
21  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1623.15  ...       1.0          3.210331
22  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1673.15  ...       0.0          3.306828
23  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1673.15  ...       1.0          3.212839
24  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1723.15  ...       0.0          3.304213
25  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1723.15  ...       1.0          3.215384
26  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1773.15  ...       0.0          3.301405
27  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1773.15  ...       1.0          3.217990
28  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1823.15  ...       0.0          3.301163
29  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1873.15  ...       0.0          3.303055
30  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1923.15  ...       0.0          3.304972
31  {'Ru': 15, 'Nb': 70, 'Ti': 15}      1973.15  ...       0.0          3.306916
32  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2023.15  ...       0.0          3.308886
33  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2073.15  ...       0.0          3.310882
34  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2123.15  ...       0.0          3.312904
35  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2173.15  ...       0.0          3.314954
36  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2223.15  ...       0.0          3.317563
37  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2223.15  ...       NaN               NaN
38  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2273.15  ...       0.0          3.323969
39  {'Ru': 15, 'Nb': 70, 'Ti': 15}      2273.15  ...       NaN               NaN

[40 rows x 6 columns]
Alloy forms BCC and B2
We want the BCC to be more stable than the B2 phase
Temperature difference between BCC and B2:  500.0
    Temperature  Phases  QuantBCC   QuantB2  TotalBCCandB2  LatticeMismatch
0        373.15  BCC+B2  0.700000  0.300000       1.000000        -0.045700
1        773.15  BCC+B2  0.700111  0.299889       1.000000        -0.044897
2       1073.15  BCC+B2  0.705322  0.294678       1.000000        -0.041659
3       1173.15  BCC+B2  0.712428  0.287572       1.000000        -0.040135
4       1273.15  BCC+B2  0.725227  0.274773       1.000000        -0.038411
5       1373.15  BCC+B2  0.745888  0.254112       1.000000        -0.036468
6       1423.15  BCC+B2  0.759918  0.240082       1.000000        -0.035401
7       1473.15  BCC+B2  0.776913  0.223087       1.000000        -0.034260
8       1523.15  BCC+B2  0.797353  0.202647       1.000000        -0.033039
9       1573.15  BCC+B2  0.821824  0.178176       1.000000        -0.031729
10      1623.15  BCC+B2  0.851036  0.148964       1.000000        -0.030327
11      1673.15  BCC+B2  0.885810  0.114190       1.000000        -0.028832
12      1723.15  BCC+B2  0.927066  0.072934       1.000000        -0.027250
13      1773.15  BCC+B2  0.975783  0.024217       1.000000        -0.025590
14      1823.15     BCC  1.000000       NaN       1.000000              NaN
15      1873.15     BCC  1.000000       NaN       1.000000              NaN
16      1923.15     BCC  1.000000       NaN       1.000000              NaN
17      1973.15     BCC  1.000000       NaN       1.000000              NaN
18      2023.15     BCC  1.000000       NaN       1.000000              NaN
19      2073.15     BCC  1.000000       NaN       1.000000              NaN
20      2123.15     BCC  1.000000       NaN       1.000000              NaN
21      2173.15     BCC  1.000000       NaN       1.000000              NaN
22      2223.15     BCC  0.965906       NaN       0.965906              NaN
23      2273.15     BCC  0.687509       NaN       0.687509              NaN
Number of Critically Assessed Ternaries:  0
Fraction of Critically Assessed Ternaries:  0.0

Number of Tentatively Assessed Ternaries:  0
Fraction of Tentatviely Assessed Ternaries:  0.0

Total Number of Assessed Ternaries:  0
Fraction of Assessed Ternaries:  0.0
Thermo-Calc Confidence Score is:  -1.0
