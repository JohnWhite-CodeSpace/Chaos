import main as mn
import numpy as np
class equation_handler():

    def __init__(self, main_frame):
        super(equation_handler,self).__init__()
        self.main_frame = main_frame
        self.constants = []


    def Set_Lorenz_Conditions(self, rho, beta, sigma):
        self.constants = {rho,beta,sigma}
        return self.constants
    def Runge_Kutta_Algorithm_4(self,initial_conditions, t_start, t_end, num_steps):
        t_values = np.linspace(t_start, t_end, num_steps)
        dt = (t_end - t_start) / num_steps
        xyz = np.zeros((num_steps, 3))
        xyz[0] = initial_conditions

        for i in range(1, num_steps):
            k1 = self.lorenz_system(t_values[i - 1], xyz[i - 1])
            k2 = self.lorenz_system(t_values[i - 1] + 0.5 * dt, xyz[i - 1] + 0.5 * dt * k1)
            k3 = self.lorenz_system(t_values[i - 1] + 0.5 * dt, xyz[i - 1] + 0.5 * dt * k2)
            k4 = self.lorenz_system(t_values[i - 1] + dt, xyz[i - 1] + dt * k3)
            xyz[i] = xyz[i - 1] + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        return t_values, xyz

    def Lorenz(self,xyz,constants):
        x, y, z = xyz
        if constants is not None:
            dxdt = self.constants[2] * (y - x)
            dydt = x * (self.constants[0] - z) - y
            dzdt = x * y - self.constants[1] * z
        return np.array([dxdt, dydt, dzdt])


    #def Get_params_for_Lorenz(self, a, b, sig, Terminal, iter):



    #def Get_params_for_Rossler(self,a, b, Terminal, iter):





