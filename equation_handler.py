import numpy as np


class Eq_Handler():

    def __init__(self):
        super(Eq_Handler, self).__init__()
        self.constantsl = {}
        self.constantsr = {}

    def set_lorenz_conditions(self, rho, beta, sigma):
        self.constantsl['rho'] = rho
        self.constantsl['beta'] = beta
        self.constantsl['sigma'] = sigma
    def lorenz(self, xyz):
        x, y, z = xyz
        dxdt = self.constantsl['sigma'] * (y - x)
        dydt = x * (self.constantsl['rho'] - z) - y
        dzdt = x * y - self.constantsl['beta'] * z
        return np.array([dxdt, dydt, dzdt])

    def runge_kutta_algorithm_4_lorenz(self, initial_conditions, t_start, t_end, num_steps):
        t_values = np.linspace(t_start, t_end, num_steps)
        dt = (t_end - t_start) / num_steps
        xyz = np.zeros((num_steps, 3))
        xyz[0] = initial_conditions

        for i in range(1, num_steps):
            k1 = self.lorenz(xyz[i - 1])
            k2 = self.lorenz(xyz[i - 1] + 0.5 * dt * k1)
            k3 = self.lorenz(xyz[i - 1] + 0.5 * dt * k2)
            k4 = self.lorenz(xyz[i - 1] + dt * k3)
            xyz[i] = xyz[i - 1] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        return t_values, xyz

    def set_roessler_conditions(self, a, b, c):
        self.constantsr['a'] = a
        self.constantsr['b'] = b
        self.constantsr['c'] = c

    def roessler(self, xyz):
        x, y, z = xyz
        dxdt = -y - z
        dydt = x + self.constantsr['a'] * y
        dzdt = self.constantsr['b'] + z * (x - self.constantsr['c'])
        return np.array([dxdt, dydt, dzdt])

    def runge_kutta_algorithm_4_roessler(self, initial_conditions, t_start, t_end, num_steps):
        t_values = np.linspace(t_start, t_end, num_steps)
        dt = (t_end - t_start) / num_steps
        xyz = np.zeros((num_steps, 3))
        xyz[0] = initial_conditions

        for i in range(1, num_steps):
            k1 = self.roessler(xyz[i - 1])
            k2 = self.roessler(xyz[i - 1] + 0.5 * dt * k1)
            k3 = self.roessler(xyz[i - 1] + 0.5 * dt * k2)
            k4 = self.roessler(xyz[i - 1] + dt * k3)
            xyz[i] = xyz[i - 1] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        return t_values, xyz


    def print_lorenz_eq(self, rho, beta, sigma):
        return f"Lorenz system:\n"\
               f"{sigma}(x-y)\n" \
               f"x({rho}-z)-y\n" \
               f"xy-{beta}z\n"

    def print_roessler_eq(self, a, b, c):
        return f"Rössler system:\n"\
               f"-x - y\n" \
               f"x + {a}y\n" \
               f"{b} + z(x -{c})\n"


