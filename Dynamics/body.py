class central_body:
    def __init__(self, name):
        if name == "Earth":
            self.name = name
            self.mu = 3.986004418e14
            self.J2 = 1.08262668e-3
            self.radius = 6378.1e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Moon":
            self.name = name
            self.mu = 4.9028e12
            self.J2 = .2027e-3
            self.radius = 1737.4e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Mars":
            self.name = name
            self.mu = 4.282837e13
            self.J2 = 1.96045e-3
            self.radius = 3389.5e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Venus":
            self.name = name
            self.mu = 3.24859e14
            self.J2 = 4.458e-6
            self.radius = 6051.8e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Mercury":
            self.name = name
            self.mu = 2.2032e13
            self.J2 = 50.3e-6
            self.radius = 2439.7e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Sun":
            self.name = name
            self.mu = 1.32712440018e20
            self.J2 = 0
            self.radius = 695700e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Jupiter":
            self.name = name
            self.mu = 1.26686534e17
            self.J2 = 14736e-6
            self.radius = 69911e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Saturn":
            self.name = name
            self.mu = 3.7931187e16
            self.J2 = 16298e-6
            self.radius = 58232e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Uranus":
            self.name = name
            self.mu = 5.793939e15
            self.J2 = 3343.43e-6
            self.radius = 25362e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Neptune":
            self.name = name
            self.mu = 6.836529e15
            self.J2 = 3411e-6
            self.radius = 24622e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        elif name == "Pluto":
            self.name = name
            self.mu = 8.71e11
            self.J2 = 0
            self.radius = 1188.3e3
            self.harmonic_coeffs = 0
            self.colors = [[0, 'rgb(40, 122, 184)'], [1, 'rgb(52, 165, 111)']]
        else:
            print("Central Body not supported")
