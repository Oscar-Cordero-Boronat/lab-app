import numpy as np
import matplotlib.pyplot as plt


class CavityInteraction:

    def __init__(
        self,
        N,
        lambda_signal,
        Lambda0_um,
        phi_R_pi,
        phi_L_pi,
        T_min,
        T_max
    ):

        self.N = N
        self.lambda_signal = lambda_signal

        self.Lambda0 = Lambda0_um * 1e-6
        self.L = N * self.Lambda0

        self.phi_R = phi_R_pi * np.pi
        self.phi_L = phi_L_pi * np.pi

        self.phi_R_pi = phi_R_pi
        self.phi_L_pi = phi_L_pi

        self.T_min = min(T_min, T_max)
        self.T_max = max(T_min, T_max)

    # ========================================================
    # Physics functions
    # ========================================================

    def refractive_index_sellmeier(self,
        wavelength_nm,
        A=2.12725,
        B=1.18431,
        C=5.14852e-2,
        D=0.6603,
        E=100.00507,
        F=9.68956e-3
    ):
        """
        Sellmeier refractive index.
        
        Parameters
        ----------
        wavelength_nm : float or ndarray
            Wavelength in nm.
        """

        wavelength_um = wavelength_nm * 1e-3
        lam_sq = wavelength_um**2

        n_sq = (
            A
            + B / (1 - C / lam_sq)
            + D / (1 - E / lam_sq)
            - F * lam_sq
        )

        return np.sqrt(n_sq)

    def delta_n(self, T, wavelength_nm):
        """
        Temperature-dependent refractive index correction.
        """

        wavelength_um = wavelength_nm * 1e-3

        a1 = np.array([9.9587, 9.9228, -8.9603, 4.1010]) * 1e-6
        a2 = np.array([-1.1882, 10.459, -9.8136, 3.1481]) * 1e-8

        dT = T - 25

        term1 = dT * (
            a1[0]
            + a1[1] / wavelength_um
            + a1[2] / wavelength_um**2
            + a1[3] / wavelength_um**3
        )

        term2 = dT**2 * (
            a2[0]
            + a2[1] / wavelength_um
            + a2[2] / wavelength_um**2
            + a2[3] / wavelength_um**3
        )

        return term1 + term2

    def refractive_index(self,wavelength_nm, T=25):
        """
        Total refractive index including thermal correction.
        """
        return (
            self.refractive_index_sellmeier(wavelength_nm)
            + self.delta_n(T, wavelength_nm)
        )

    def wavevector(self, wavelength_nm, T):

        wavelength_m = wavelength_nm * 1e-9

        n = self.refractive_index(wavelength_nm, T)

        return 2 * np.pi * n / wavelength_m

    def poling_period(self, T, T0=25, alpha_z=8.7e-6):

        return self.Lambda0 * (1 + alpha_z * (T - T0))

    def delta_k(self, T):

        lambda_pump_nm = self.lambda_signal / 2

        k_pump = self.wavevector(lambda_pump_nm, T)
        k_signal = self.wavevector(self.lambda_signal, T)

        Lambda = self.poling_period(T)

        return (
            k_pump
            - 2 * k_signal
            - 2 * np.pi / Lambda
        )

    def single_pass(self, T):

        dk = self.delta_k(T)

        return (
            self.L
            * np.exp(1j * dk * self.L / 2)
            * np.sinc((dk * self.L / 2) / np.pi)
        )

    def cavity(self, T, flag=False):

        dk = self.delta_k(T)

        rho = np.sqrt(0.945)
        tau = np.sqrt(0.055)

        term1 = (
            self.L
            * np.exp(1j * dk * self.L / 2)
            * np.sinc((dk * self.L / 2) / np.pi)
        )

        term2 = (
            np.exp(-1j * (self.phi_L + self.L * dk))
            + np.exp(-1j * (self.phi_R + 2 * self.L * dk))
        )

        if flag:
            term2 = (
            np.exp(-1j * (0 + self.L * dk))
            + np.exp(-1j * (0 + 2 * self.L * dk))
        )

        return (
            1j
            * tau
            * term1
            * term2
            / (1 - rho)
        )

    def double_resonance_T(self, Ts):

        L = self.poling_period(Ts) * self.N

        lambda_pump_nm = self.lambda_signal / 2

        k_pump = self.wavevector(lambda_pump_nm, Ts)
        k_signal = self.wavevector(self.lambda_signal, Ts)

        phase = (
            (2 * L) * (k_pump - 2 * k_signal)
            + 2 * self.phi_L
            + 2 * self.phi_R
        ) % (2 * np.pi)
        indices = np.where(np.diff(phase) < -2)[0]        
        return indices, Ts[indices]


    # ========================================================
    # Plot
    # ========================================================

    def plot(self):

        Ts = np.linspace(0, 70, 2001)
        Ts_map = np.linspace(0, 70, 1001)

        fig, (ax1, ax2) = plt.subplots(
            1,
            2,
            figsize=(14, 5),
            gridspec_kw={"width_ratios": [1.25, 1]}
        )

        # ----------------------------------------------------
        # Left plot
        # ----------------------------------------------------

        field1 = self.single_pass(Ts)
        abs_field1 = np.abs(field1)**2
        ax1.plot(
            Ts,
            abs_field1 / np.max(abs_field1),
            linewidth=2,
            label="Single pass"
        )

        ax1.set_title(f"Length Crystal = {self.Lambda0 * self.N * 1e3:.1f} mm", fontsize=20)

        field2_ref = self.cavity(Ts, flag=True)
        normalization_factor = np.max(np.abs(field2_ref)**2)



        field2 = self.cavity(Ts)
        abs_field2 = np.abs(field2)**2 / normalization_factor

        ax1.plot(
            Ts,
            abs_field2,
            linewidth=2,
            label="Cavity"
        )

        indices, resonance_Ts = self.double_resonance_T(Ts)

        valid_mask = (
            (resonance_Ts >= self.T_min)
            & (resonance_Ts <= self.T_max)
        )


        for i, T_res in enumerate(resonance_Ts):

            ax1.axvline(
                T_res,
                linestyle="--",
                linewidth=1,
                alpha=0.5,
                color="red",
                label="Double resonance" if i == 0 else None
            )

        ax1.axvspan(
            self.T_min,
            self.T_max,
            color="gray",
            alpha=0.2
        )

        ax1.grid(True, alpha=0.3)

        ax1.set_xlabel("Temperature (°C)", fontsize=20)
        ax1.set_ylabel("Normalized interaction strength", fontsize=20)
        ax1.tick_params(axis='both', labelsize=15)
        ax1.legend(fontsize=15)


        # ----------------------------------------------------
        # Right plot
        # ----------------------------------------------------

        phi_values = np.linspace(0, 2 * np.pi, 25)

        max_values = np.zeros((25, 25))

        for i, phi_R in enumerate(phi_values):
            for j, phi_L in enumerate(phi_values):

                self.phi_R = phi_R
                self.phi_L = phi_L

                field = self.cavity(Ts_map)
                abs_field = np.abs(field)**2 / normalization_factor
                indices, resonance_Ts = self.double_resonance_T(Ts_map)
                valid_mask = (
                    (resonance_Ts >= self.T_min)
                    & (resonance_Ts <= self.T_max)
                )


                valid_indices = indices[valid_mask]

                if len(valid_indices) > 0:
                    max_values[i, j] = np.max(abs_field[valid_indices])
                else:
                    max_values[i, j] = np.nan

        im = ax2.imshow(
            max_values,
            origin="lower",
            aspect="equal",
            cmap="RdBu_r",
            interpolation="bicubic",
            vmin=0,
            vmax=1,
            extent=[0, 2, 0, 2]
        )

        fig.colorbar(im, ax=ax2)

        ax2.scatter(
            self.phi_L_pi,
            self.phi_R_pi,
            s=150,
            color="black",
            marker="x",
            linewidths=4
        )

        ticks = np.arange(0, 2.1, 0.5)

        labels = [
            r"0",
            r"$\pi/2$",
            r"$\pi$",
            r"$3\pi/2$",
            r"$2\pi$"
        ]

        ax2.set_xticks(ticks, labels, fontsize=20)
        ax2.set_yticks(ticks, labels, fontsize=20)

        ax2.set_xlabel(r"$\phi_L$", fontsize=20)
        ax2.set_ylabel(r"$\phi_R$", fontsize=20)

        plt.tight_layout()

        return fig