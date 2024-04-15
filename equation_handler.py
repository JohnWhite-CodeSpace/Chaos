import numpy as np


class Eq_Handler:
    """
    Class designed for numeric operations based on  Lorenz and Roessler attractors theorem

    Attributes
        constantsl - lorenz constants array
        constantsr - roessler constants array

    Methods
        set_lorenz_conditions(self, rho, beta, sigma) -  Sets Lorenz rho, beta & sigma parameters of constantsl array to given values\n
        lorenz(self, xyz) - Calculates difference quotients based on Lorenz attractor equations to be used in Runge-Kutta algorithm\n
        set_roessler_conditions(self, a, b, c) - Sets Roessler a, b & c parameters of constantsr array to given values\n
        roessler(self, xyz) - Calculates difference quotients based on Roessler attractor equations to be used in Runge-Kutta algorithm\n
        print_lorenz_eq(self, rho, beta, sigma) - Outputs Lorenz attractor equations in a legible form
        print_roessler_eq(self, a, b, c) - Outputs Roessler attractor equations in a legible form\n
        runge_kutta_algorithm_4_lorenz(self, initial_conditions, t_start, t_end, num_steps) - uses 4th order Runge-Kutta algorithm to solve Lorenz attractor equations numerically, calculating the XYZ
        points for Roessler attractor of given parameters\n
        runge_kutta_algorithm_4_roessler(self, initial_conditions, t_start, t_end, num_steps) -  uses 4th order Runge-Kutta algorithm to solve Roessler attractor equations numerically, calculating the XYZ
        points for Roessler attractor of given parameters\n
    """
    def __init__(self):
        super(Eq_Handler, self).__init__()
        self.constantsl = {}
        self.constantsr = {}

    def set_lorenz_conditions(self, rho, beta, sigma):
        """
        Sets Lorenz rho, beta & sigma parameters of constantsl array to given values

        :param rho: rho parameter of Lorenz attractor equation
        :param beta: beta parameter of Lorenz attractor equation
        :param sigma: sigma parameter of Lorenz attractor equation
        :return: array of Lorenz parameters
        """

        self.constantsl['rho'] = rho
        self.constantsl['beta'] = beta
        self.constantsl['sigma'] = sigma
        print(self.constantsl)

    def lorenz(self, xyz):
        """
        Calculates difference quotients based on Lorenz attractor equations to be used in Runge-Kutta algorithm

        :param xyz: temporary x, y, z values as an array
        :return: array of difference quotients as an array
        """
        x, y, z = xyz
        dxdt = self.constantsl['sigma'] * (y - x)
        dydt = x * (self.constantsl['rho'] - z) - y
        dzdt = x * y - self.constantsl['beta'] * z
        return np.array([dxdt, dydt, dzdt])

    def set_roessler_conditions(self, a, b, c):
        """
        Sets Roessler a, b & c parameters of constantsr array to given values

        :param a: a parameter of Roessler attractor equation
        :param b: b parameter of Roessler attractor equation
        :param c: c parameter of Roessler attractor equation
        :return: array of Roessler parameters
        """
        self.constantsr['a'] = a
        self.constantsr['b'] = b
        self.constantsr['c'] = c
        print("kutas")

    def roessler(self, xyz):
        """
        Calculates difference quotients based on Roessler attractor equations to be used in Runge-Kutta algorithm

        :param xyz: temporary x, y, z values as an array
        :return: array of difference quotients as an array
        """
        x, y, z = xyz
        dxdt = -y - z
        dydt = x + self.constantsr['a'] * y
        dzdt = self.constantsr['b'] + z * (x - self.constantsr['c'])
        return np.array([dxdt, dydt, dzdt])

    def print_lorenz_eq(self, rho, beta, sigma):
        """
        Outputs Lorenz attractor equations in a legible form

        :param rho: rho parameter of Lorenz attractor equation
        :param beta: beta parameter of Lorenz attractor equation
        :param sigma: sigma parameter of Lorenz attractor equation
        :return: string representation of Lorenz attractor equation
        """
        return f"Lorenz system:\n" \
               f"dxdt = {sigma}(x-y)\n" \
               f"dydt = x({rho}-z)-y\n" \
               f"dzdt = xy-{beta}z\n"

    def print_roessler_eq(self, a, b, c):
        """
        Outputs Roessler attractor equations in a legible form

        :param a: a parameter of Roessler attractor equation
        :param b: b parameter of Roessler attractor equation
        :param c: c parameter of Roessler attractor equation
        :return: string representation of Roessler attractor equation
        """
        return f"Rössler system:\n" \
               f"-x - y\n" \
               f"x + {a}y\n" \
               f"{b} + z(x -{c})\n"

    def runge_kutta_algorithm_4_lorenz(self, init_conditions, t_start, t_end, num_steps):
        """
        Uses 4th order Runge-Kutta algorithm to solve Lorenz attractor equations numerically, calculating the XYZ
        points for lorenz attractor of given parameters

        :param init_conditions: initial XYZ values for Lorenz attractor
        :param t_start: initial time for Lorenz attractor
        :param t_end: end time for Lorenz attractor
        :param num_steps: number of steps determining the density of points
        :return: Array of evenly spaced numbers based on stop, start and step conditions,  Array of XYZ points for Lorenz attractor of given parameters
        """
        t_values = np.linspace(t_start, t_end, num_steps)
        dt = (t_end - t_start) / num_steps
        xyz = np.zeros((num_steps, 3))
        xyz[0] = init_conditions

        for i in range(1, num_steps):
            k1 = self.lorenz(xyz[i - 1])
            k2 = self.lorenz(xyz[i - 1] + 0.5 * dt * k1)
            k3 = self.lorenz(xyz[i - 1] + 0.5 * dt * k2)
            k4 = self.lorenz(xyz[i - 1] + dt * k3)
            xyz[i] = xyz[i - 1] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        return t_values, xyz

    def runge_kutta_algorithm_4_roessler(self, init_conditions, t_start, t_end, num_steps):
        """
        Uses 4th order Runge-Kutta algorithm to solve Roessler attractor equations numerically, calculating the XYZ
        points for Roessler attractor of given parameters

        :param init_conditions: initial XYZ values for Roessler attractor
        :param t_start: initial time for Roessler attractor
        :param t_end: end time for Roessler attractor
        :param num_steps: number of steps determining the density of points
        :return: Array of evenly spaced numbers based on stop, start and step conditions,  Array of XYZ points for Roessler attractor of given parameters
        """
        t_values = np.linspace(t_start, t_end, num_steps)
        dt = (t_end - t_start) / num_steps
        xyz = np.zeros((num_steps, 3))
        xyz[0] = init_conditions

        for i in range(1, num_steps):
            k1 = self.roessler(xyz[i - 1])
            k2 = self.roessler(xyz[i - 1] + 0.5 * dt * k1)
            k3 = self.roessler(xyz[i - 1] + 0.5 * dt * k2)
            k4 = self.roessler(xyz[i - 1] + dt * k3)
            xyz[i] = xyz[i - 1] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        return t_values, xyz