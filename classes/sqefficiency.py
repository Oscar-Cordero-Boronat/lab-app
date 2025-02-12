import numpy as np
import matplotlib.pyplot as plt
from typing import Union, List
from scipy.optimize import curve_fit

class SqEfficiency:
    def __init__(self, 
                 power: np.ndarray, 
                 sq_data: np.ndarray, 
                 asq_data: np.ndarray, 
                 phase_noise: bool = False, 
                 detection_frequency: float = 5, 
                 decay_rate_cavity: float = 20.3,
                 y_axis = np.array([-3,15]),
                 P_th = ""
                                            ):
        """
        Initializes the SqEfficiency object with input data for power, squeezing, and antisqueezing values.
        
        Args:
            power (np.ndarray): Array of pump power values (mW).
            sq_data (np.ndarray): Array of squeezing data (dB).
            asq_data (np.ndarray): Array of antisqueezing data (dB).
            phase_noise (bool): Flag to indicate if phase noise should be considered in fitting.
            detection_frequency (float): Detection frequency (MHz).
            decay_rate_cavity (float): Decay rate of the cavity (MHz).
        """
        self.power = self._validate_input(power, np.ndarray, 'Power')
        self.sq_data = self._validate_input(sq_data, np.ndarray, 'Squeezing Data')
        self.asq_data = self._validate_input(asq_data, np.ndarray, 'Antisqueezing Data')
        self.phase_noise = self._validate_boolean(phase_noise, 'Phase Noise')
        self.omega = self._validate_float(detection_frequency, 'Detection Frequency', min_value=0)
        self.gamma = self._validate_float(decay_rate_cavity, 'Decay Rate Cavity', min_value=0)
        self.y_axis = y_axis
        if P_th:
           self.P_th = float(P_th)
        else: 
            self.P_th = P_th

        if (self.phase_noise and len(self.sq_data) + len(self.asq_data) < 3):
            raise KeyError(f"It is required at least 2 squeezing and antisqueezing data") 
        elif  len(self.sq_data) != len(self.asq_data) or len(self.sq_data) != len(self.power):
            raise KeyError(f"You should have the same number of points in squeezing data, antisqueezing data and pump power") 
        elif (not self.phase_noise and len(self.sq_data) + len(self.asq_data) < 1):
            raise KeyError(f"It is required at least 1 squeezing and antisqueezing data") 
        else:
            # Fit the curve and plot the results
            self.fit_curve_noise()

    def _validate_input(self, data: Union[np.ndarray, List], expected_type: type, name: str) -> np.ndarray:
        """
        Validate that input data is of the expected type and has the correct shape.

        Args:
            data (Union[np.ndarray, List]): The input data to be validated.
            expected_type (type): The expected type of the input data.
            name (str): Name of the data being validated, used for error messages.

        Returns:
            np.ndarray: The validated input data.
        """
        if not isinstance(data, expected_type):
            raise ValueError(f"{name} must be of type {expected_type}.")
        
        # Ensure data is a numpy array for consistency
        if isinstance(data, list):
            data = np.array(data)
        
        return data

    def _validate_boolean(self, value: bool, name: str) -> bool:
        """
        Validate that the value is a boolean.

        Args:
            value (bool): The value to validate.
            name (str): The name used for error reporting.

        Returns:
            bool: The validated boolean value.
        """
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be of type bool.")
        return value

    def _validate_float(self, value: float, name: str, min_value: float = None, max_value: float = None) -> float:
        """
        Validate that the value is a float and within the specified range.

        Args:
            value (float): The value to validate.
            name (str): The name used for error reporting.
            min_value (float, optional): Minimum allowed value for the parameter.
            max_value (float, optional): Maximum allowed value for the parameter.

        Returns:
            float: The validated float value.
        """
        if not isinstance(value, (float, int)):
            raise ValueError(f"{name} must be of type float.")
        value = float(value)  # Convert to float if it's an integer
        
        if min_value is not None and value < min_value:
            raise ValueError(f"{name} must be greater than or equal to {min_value}.")
        if max_value is not None and value > max_value:
            raise ValueError(f"{name} must be less than or equal to {max_value}.")
        
        return value

    def fit_curve_noise(self):
        """
        Fits the model to the squeezing and antisqueezing data using curve fitting.

        Updates the fitted parameters: eta, P_th, and phase_noise.
        """
        if not self.P_th:
            initial_guess = [0.8, 50, 0.2] if self.phase_noise else [0.8, 50]
            param_bounds = ([0, 0, 0], [1, np.inf, np.pi / 4]) if self.phase_noise else ([0, 0], [1, np.inf])
        else:
            initial_guess = [0.8, self.P_th, 0.2] if self.phase_noise else [0.8, self.P_th]
            param_bounds = ([0, self.P_th - 1e-3, 0], [1, self.P_th + 1e-3, np.pi / 4]) if self.phase_noise else ([0, self.P_th - 1e-3], [1, self.P_th + 1e-3])
        
        # Fit model to both sq and asq data
        result = curve_fit(
            lambda p, eta, P_th, phase_noise=None: self.combined_residuals_noise((eta, P_th, phase_noise), p)
            if self.phase_noise else self.combined_residuals_noise_no_phase((eta, P_th), p),
            self.power,
            np.zeros(2 * len(self.power)),
            p0=initial_guess,
            bounds=param_bounds
        )

        # Extract fitted parameters
        if self.phase_noise:
            self.eta_fit, self.P_th_fit, self.phase_noise_fit = result[0]
        else:
            self.eta_fit, self.P_th_fit = result[0]
            self.phase_noise_fit = 0  # Set phase noise to 0 if not fitting it

        # Generate fitted curves for plotting
        self.power_fit = np.linspace(0, self.P_th_fit, 1000)
        self.sq_fit, self.asq_fit = self.sq_asq_model_noise(self.power_fit, self.eta_fit, self.P_th_fit, self.phase_noise_fit)

    

    def sq_asq_model_noise(self, power: np.ndarray, eta: float, P_th: float, phase_noise: float) -> tuple:
        """
        Model for squeezing and antisqueezing based on power, eta, P_th, and phase noise.

        Args:
            power (np.ndarray): Array of power values.
            eta (float): Squeezing efficiency.
            P_th (float): Threshold power.
            phase_noise (float): Phase noise (if any).

        Returns:
            tuple: Squeezing and antisqueezing values (dB).
        """
        c = np.sqrt(power / P_th)
        sq = 1 - eta * (4 * c) / ((1 + c)**2 + (self.omega / self.gamma)**2)
        asq = 1 + eta * (4 * c) / ((1 - c)**2 + (self.omega / self.gamma)**2)

        if self.phase_noise:
            sq, asq = 10 * np.log10(sq * np.cos(phase_noise)**2 + asq * np.sin(phase_noise)**2), \
                      10 * np.log10(asq * np.cos(phase_noise)**2 + sq * np.sin(phase_noise)**2)
        else:
            sq = 10 * np.log10(sq)
            asq = 10 * np.log10(asq)

        return sq, asq

    def combined_residuals_noise(self, params: tuple, power: np.ndarray) -> np.ndarray:
        """
        Computes the residuals (difference between the data and the model) for fitting.
        
        Args:
            params (tuple): Parameters (eta, P_th, phase_noise) to be fitted.
            power (np.ndarray): Array of power values.

        Returns:
            np.ndarray: Residuals for fitting.
        """
        eta, P_th, phase_noise = params
        sq, asq = self.sq_asq_model_noise(power, eta, P_th, phase_noise)
        residuals = np.concatenate((sq - self.sq_data, asq - self.asq_data))
        return residuals

    def combined_residuals_noise_no_phase(self, params: tuple, power: np.ndarray) -> np.ndarray:
        """
        Computes the residuals without considering phase noise.

        Args:
            params (tuple): Parameters (eta, P_th) to be fitted.
            power (np.ndarray): Array of power values.

        Returns:
            np.ndarray: Residuals for fitting.
        """
        eta, P_th = params
        sq, asq = self.sq_asq_model_noise(power, eta, P_th, 0)  # No phase noise
        residuals = np.concatenate((sq - self.sq_data, asq - self.asq_data))
        return residuals
    

    def plot_noise(self):
        fig, ax = plt.subplots()
        ax.plot(self.power, self.sq_data, 'or', label="Squeezing Data")
        ax.plot(self.power, self.asq_data, 'ob', label="Antisqueezing Data")
        ax.plot(self.power_fit, self.sq_fit, 'r-', label="Squeezing Fit")
        ax.plot(self.power_fit, self.asq_fit, 'b-', label="Antisqueezing Fit")
        ax.set_xlabel("Power [mW]")
        ax.set_ylabel("Variance [dB]")
        ax.set_xlim([0, self.P_th_fit])
        ymax = self.y_axis[1] // 2.5
        ymin = self.y_axis[0] // 2.5
        ax.set_yticks(np.linspace(ymin * 2.5, ymax * 2.5, int(ymax - ymin) + 1))
        ax.set_ylim(self.y_axis)
        ax.legend()
        ax.set_title(rf"$\eta = {self.eta_fit * 100:.2f}\text{{\%}}~~~~P_\text{{th}} = {self.P_th_fit:.2f}\,\text{{mW}}~~~~\varepsilon = {self.phase_noise_fit * 1e3:.2f}\,\text{{mrad}}$")
        ax.grid()
        return fig
