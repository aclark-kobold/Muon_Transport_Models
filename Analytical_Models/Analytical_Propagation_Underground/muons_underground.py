import numpy as np
import matplotlib.pyplot
import scipy.integrate as integrate


### Global Variables ###
A_LOSS = 0.25            # GeV per m.w.e.   (ionization loss)
B_LOSS = 0.36e-3         # per m.w.e.       (radiative loss)
EPS = A_LOSS / B_LOSS    # GeV
P = 1#Density

### Surface Muon Spectrum Analytical Model ###
#Can be replaced with prefered model
#from ..Analytical_Models.guan_model import modified_gaisser_formula
def surface_spectrum(E_s, theta):
    "Guan model of muon surface spectrum in units of m^-2*s^-1*sr^-1*GeV^-1"
   
    """
    dF/dSAdE = [m^-2*s^-1*sr^-1*GeV^-1]
    """
    p_1 = 0.102573 ; p_2 = -0.068287 ; p_3 = 0.958633; p_4 = 0.0407253 ; p_5 = 0.817285

    cos_star = np.sqrt((np.cos(theta)**2 + p_1**2 + (p_2 * np.cos(theta)**p_3) + (p_4 * np.cos(theta)**p_5)) / (1 + p_1**2 + p_2 + p_4))

    E_star = E_s * (1 + (3.64/(E_s*cos_star**1.29)))

    return 10000 * 0.14 * E_star**-2.7 * ( (1/(1+((1.1*E_s*cos_star)/115))) + (0.054/(1+((1.1*E_s*cos_star)/850))) )

### Basic Functions ###
def slant_depth(h, theta):
    "Amount of material a Muon has to travel underground changes with zenith"
    return h/np.cos(theta)

def surface_energy(E_u, X):
    """Surface energy (GeV) of a muon that arrives with energy E_u after slant depth X."""
    return (E_u + EPS) * np.exp(B_LOSS * X) - EPS

def minimum_surface_energy(X):
    "Eps = critical energy in material; eps = a (Ionization loss) / b (radiative loss)"
    "Minimum surface energy required to reach a depth X"
    return EPS * (np.exp**(B_LOSS*X) - 1)

def underground_muon_spectrum(E_u, theta, h):
    "Underground differential energy spectrum"
    X = slant_depth(h, theta)
    return np.exp**(B_LOSS * X) * surface_spectrum(surface_energy(E_u, X), theta) * np.sin(theta)

def flux(h,theta):
    result = 2*np.pi*integrate.quad(underground_muon_spectrum, 0, np.inf, args = (h, theta))[0]
    return result

h_list = [0, 100, 200, 300, 400, 500]
for h in h_list:
    print(flux(h, 0))
