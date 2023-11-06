import numpy as np
import scipy.integrate as int

class Body:
    def __init__(self, name, states, warn=False):
        if (((name != "Earth") and (name != "Venus") and (name != "Mars") and (name != "Pluto")) and warn):
            print(f"Warning: Atmosphere not supported for {name}")
            if name != "Earth":
                print(f"Warning: {name} centered {name} fixed frame not supported")
        self.states = states
        self.curr_idx = 0
        self.state = self.states[:,self.curr_idx]
        if name == "Earth":
            self.name = name
            self.radius = 6378.1e3
            self.mu = 3.986004418e14
            self.J2 = (1082.63e-6)*self.mu*self.radius**2
            self.rho0 = 1.225
            self.scaleHeight = 8500
            self.colors = [[0, 'rgb(159,193,100)'], [1, 'rgb(107,147,214)']]
        elif name == "Moon":
            self.name = name
            self.radius = 1737.4e3
            self.mu = 4.9028e12
            self.J2 = (202.7e-6)*self.mu*self.radius**2
            self.colors = [[0, 'rgb(148, 144, 141)'], [1, 'rgb(240, 240, 240)']]
        elif name == "Mars":
            self.name = name
            self.radius = 3389.5e3
            self.mu = 4.282837e13
            self.J2 = (1960.45e-6)*self.mu*self.radius**2
            self.rho0 = .020
            self.scaleHeight = 11.1e3
            self.colors = [[0, 'rgb(193,68,14)'], [1, 'rgb(240,231,231)']]
        elif name == "Venus":
            self.name = name
            self.radius = 6051.8e3
            self.mu = 3.24859e14
            self.J2 = (4.458e-6)*self.mu*self.radius**2
            self.rho0 = 65
            self.scaleHeight = 15.9e3
            self.colors = [[0, 'rgb(193,143,23)'], [1, 'rgb(231,213,32)']]
        elif name == "Mercury":
            self.name = name
            self.radius = 2439.7e3
            self.mu = 2.2032e13
            self.J2 = (50.3e-6)*self.mu*self.radius**2
            self.colors = [[0, 'rgb(104,105,109)'], [1, 'rgb(231,232,236)']]
        elif name == "Sun":
            self.name = name
            self.radius = 695700e3
            self.mu = 1.32712440018e20
            self.J2 = 0
            self.colors = [[0, 'rgb(255, 228, 132)'], [1, 'rgb(209, 64, 9)']]
        elif name == "Jupiter":
            self.name = name
            self.radius = 69911e3
            self.mu = 1.26686534e17
            self.J2 = (14736e-6)*self.mu*self.radius**2
            self.colors = [[0, 'rgb(165,145,134)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Saturn":
            self.name = name
            self.radius = 58232e3
            self.mu = 3.7931187e16
            self.J2 = (16298e-6)*self.mu*self.radius**2
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(227,220,203)']]
        elif name == "Uranus":
            self.name = name
            self.radius = 25362e3
            self.mu = 5.793939e15
            self.J2 = (3343.43e-6)*self.mu*self.radius**2
            self.colors = [[0, 'rgb(248,248,255)'], [1, 'rgb(209,231,231)']]
        elif name == "Neptune":
            self.name = name
            self.radius = 24622e3
            self.mu = 6.836529e15
            self.J2 = (3411e-6)*self.mu*self.radius**2
            self.colors = [[0, 'rgb(39,70,135)'], [1, 'rgb(133,173,219)']]
        elif name == "Pluto":
            self.name = name
            self.radius = 1188.3e3
            self.mu = 8.71e11
            self.J2 = 0
            self.rho0 = 1.3 / (8314/28 * 30)
            self.scaleHeight = 50e3
            self.colors = [[0, 'rgb(255,241,213)'], [1, 'rgb(204,186,153)']]
        else:
            print("Body not supported")

    def update_state(self, bodies, dt, curr_true):
        if curr_true:
            self.curr_idx += 1
            self.state = self.states[:,self.curr_idx]
        else:
            self.state = solve_n_body(self, bodies, dt)

def orbit_ode(state, t, self, bodies):
    ax, ay, az = 0, 0, 0
    for body in bodies:
        if body != self:
            rel_state = state - body.state
            r = np.linalg.norm(rel_state[0:3])
            ax += -body.mu*rel_state[0]/r**3
            ay += -body.mu*rel_state[1]/r**3
            az += -body.mu*rel_state[2]/r**3
    return np.array([state[3], state[4], state[5], ax, ay, az])

def solve_n_body(self, bodies, dt):
    return int.odeint(orbit_ode, self.state, [0,dt], args = (self, bodies),rtol=1e-13, atol=1e-13)[1]