import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class Gain:
    def __init__(self, pump_power, V, V0, y_axis = [0,50]):
        self.P = np.array(pump_power)
        self.V = np.array(V)
        self.V0 = np.array(V0)
        self.G = self.V / self.V0
        self.log_G = np.log(self.G)
        self.y_axis = y_axis

        if len(self.V) != len(self.V0) or len(self.V) != len(self.P):
            raise KeyError("Pump power, α², and α₀² should have the same number of points")
        else:
            # Fit the curve and plot the results
            self.fit_Pth()


    def gain_function(self, P, P_th):
        return 1 / (1 - (P / P_th)**.5) ** 2
    

    def fit_function(self, P, P_th):
        return np.log(1 / (1 - (P / P_th)**.5) ** 2)
    

    def fit_Pth(self, initial_guess=40):
        # Fit the threshold power P_th
        params, _ = curve_fit(self.fit_function, self.P, self.log_G, p0=[initial_guess])
        self.P_th_fitted = params[0]
    



    def plot_fit(self):
        self.P_fit = np.linspace(0, self.P_th_fitted, 500)
        self.V_fit = self.gain_function(self.P_fit, self.P_th_fitted)

        fig, ax = plt.subplots()
        ax.plot(self.P, self.G, 'or', label="Gain Data")
        ax.plot(self.P_fit, self.V_fit, 'r-', label="Gain Fit")

        ax.set_xlabel("Power [mW]")
        ax.set_ylabel("Gain")        
        ax.set_ylim(self.y_axis)
        ax.set_xlim([0, self.P_th_fitted])
        ax.grid()
        ax.legend()
        return fig
    
    def plot_fit_log(self):
        self.P_fit = np.linspace(0, self.P_th_fitted, 5000)
        self.V_fit = self.gain_function(self.P_fit, self.P_th_fitted)

        fig, ax = plt.subplots()
        ax.semilogy(self.P, self.G, 'or', label="Gain Data")
        ax.semilogy(self.P_fit, self.V_fit, 'r-', label="Gain Fit")

        ax.set_xlabel("Power [mW]")
        ax.set_ylabel("Gain")        
        ax.set_ylim(self.y_axis)
        ax.set_xlim([0, self.P_th_fitted])
        ax.grid()
        ax.legend()
        return fig
