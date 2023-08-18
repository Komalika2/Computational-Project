"""
MM209.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PzAemkWRF1Jnb8jcTDU7Twcrw_bmk1ep
"""
import numpy as np
import matplotlib.pyplot as plt

T = 700 +273
delg0_CO = -114.4e3 - 85.5 * T
delg0_CO2 = -395.5e3 - 0.5 *T
R = 8.314

pCO_by_pCO2 = np.linspace(1,6,50)
p_total = 0.5

pCO2 = p_total/ (1.0+pCO_by_pCO2)
pCO = p_total - pCO2

"""
C + CO2 = 2CO

Keq1 = (pCO)^2/(a_C*pC02)

"""

delg0_1 = 2*delg0_CO - delg0_CO2
Keq1 = np.exp(-delg0_1/(R*T))
a_C_gas = (pCO**2)/(Keq1*pCO2)

logk  = 2000/T - 0.8;
k = 10.0**logk
wt_per_C = 0.25;
xC = (wt_per_C/12.0)/(100/55.85)     #Formula valid for dilute solutions
xC_s =  xC;

for i in range(10):
  xC_s = (a_C_gas/k) * (1.0- xC_s-12*(xC_s**2)) / (1.0 + 2*xC_s)
  wt_per_C_s =  xC_s *12.0*(100/55.85)

"""
Partial Pressure of Oxygen

CO + 0.5 O2 = CO2

Keq2 = (pCO2)/(pCO*pO2^2)

"""

delg0_2 = delg0_CO2 - delg0_CO
keq2 = np.exp(-delg0_2/(R*T))
pO2 =  (pCO2/(pCO*keq2))**2.0

"""
To check Oxidation of Fe

Fe + 0.5O2 = FeO

Keq3 = (pFeO)/(pFe*(pO2)^2)

"""

delg0_3 = -264.4e3 + T*64.0
delg = (delg0_3 + 8.314 * T  * np.log(1.0/(pO2**0.5)))/1000.0

wt_perCmin = float(input("Enter the lower limit of desired Wt% of Carbon "))
wt_perCmax = float(input("Enter the upper limit of desired Wt% of Carbon "))
ratio_allowed = []
for i in range(len(wt_per_C_s)):
  if wt_perCmin < wt_per_C_s[i] and wt_perCmax > wt_per_C_s[i]:
    if delg[i] > 0:
      ratio_allowed.append(pCO_by_pCO2[i])

if len(ratio_allowed) == 0:
  print("No suitable pCO/pCO2 values are possible to deposit desired Wt% of C. Please Change Total Pressure or Temperature")
else:
  print("Allowed values of CO/CO2 composition ratio are from {} to {} for Total pressure of {} Pa".format(min(ratio_allowed),max(ratio_allowed),p_total))

fig, (ax1, ax2, ax3) = plt.subplots(1,3)
fig.suptitle('P_total = {} Pa ; Temperature = {} K'.format(p_total,T))
ax1.plot(pCO_by_pCO2,a_C_gas)
ax1.set_xlabel("pCO/pCO2")
ax1.set_ylabel("Activity of C (gas)")
ax2.plot(pCO_by_pCO2, wt_per_C_s)
ax2.set_xlabel("pCO/pCO2")
ax2.set_ylabel("Wt% of C")
ax3.plot(pCO_by_pCO2, delg)
ax3.set_ylabel("ΔGf[FeO] in kJ/mol ")
ax3.set_xlabel("pCO/pCO2")
plt.show()