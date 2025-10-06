#Write a program to explore the properties of a few elementary Particles.
#The program must contain a Base class Particle and two Child classes, Proton and Alpha, that inherit from it.

#--- Specifications
#- instances of the class Particle must be initialized with their mass, charge, and name
#- the class constructor must also accept (optionally) and store one and only one of the following quantities: energy, momentum, beta or gamma
#- whatever the choice, the user should be able to read and set any of the
#  above mentioned quantities using just the '.' (dot) operator e.g.
#  print(my_particle.energy), my_particle.beta = 0.5
#- attempts to set non physical values should be rejected
#- the Particle class must have a method to print the Particle information in
#  a formatted way
#- the child classes Alpha and Protons must use class attributes to store their mass, charge and name

import math
from loguru import logger

class Particle:
    def __init__(self, *, energy=None, momentum=None, beta=None, gamma=None):
        """
        Initialize a particle with mass, charge, and name (from child class)
        Optionally, set ONE of energy, momentum, beta, gamma.
        """
        # Questo comando permette di sapere quante quantità vengono inizializzate, se sono più di una da errore
        quantities = [energy, momentum, beta, gamma]
        if sum(q is not None for q in quantities) > 1:
            raise ValueError("Set only one quantity among energy, momentum, beta, gamma.")

        # Default momentum = 0
        self._momentum = 0.0

        # Inizializza la quantità scelta
        if momentum is not None:
            self.momentum = momentum
        elif energy is not None:
            self.energy = energy
        elif beta is not None:
            self.beta = beta
        elif gamma is not None:
            self.gamma = gamma
        # Se nessuna quantità è passata, momentum = 0

    # --- CLASS ATTRIBUTES FOR CHILDREN ---
    @property
    def mass(self):
        return self.__class__.mass

    @property
    def charge(self):
        return self.__class__.charge

    @property
    def name(self):
        return self.__class__.name

    # --- ENERGY ---
    @property
    def energy(self):
        return math.sqrt(self._momentum**2 + self.mass**2)

    @energy.setter
    def energy(self, E):
        if E < self.mass:
            raise ValueError("Energy must be >= rest mass.")
        self._momentum = math.sqrt(E**2 - self.mass**2)

    # --- MOMENTUM ---
    @property
    def momentum(self):
        return self._momentum

    @momentum.setter
    def momentum(self, p):
        if p < 0:
            raise ValueError("Momentum cannot be negative.")
        self._momentum = p

    # --- BETA ---
    @property
    def beta(self):
        return self._momentum / self.energy

    @beta.setter
    def beta(self, b):
        if not (0 <= b < 1):
            raise ValueError("Beta must be between 0 and 1.")
        gamma = 1 / math.sqrt(1 - b**2)
        self._momentum = self.mass * b * gamma

    # --- GAMMA ---
    @property
    def gamma(self):
        return self.energy / self.mass

    @gamma.setter
    def gamma(self, g):
        if g < 1:
            raise ValueError("Gamma must be >= 1")
        self._momentum = self.mass * math.sqrt(g**2 - 1)

    # --- PRINT INFO ---
    def print_info(self):
        logger.info(f"Particle: {self.name}")
        logger.info(f"  Mass     : {self.mass:.3f} MeV/c²")
        logger.info(f"  Charge   : {self.charge:+} e")
        logger.info(f"  Momentum : {self.momentum:.3f} MeV/c")
        logger.info(f"  Energy   : {self.energy:.3f} MeV")
        logger.info(f"  Beta     : {self.beta:.5f}")
        logger.info(f"  Gamma    : {self.gamma:.5f}")


# === CHILD CLASSES WITH CLASS ATTRIBUTES ===
class Proton(Particle):
    mass = 938.272
    charge = +1
    name = "proton"

class Alpha(Particle):
    mass = 3727.379
    charge = +2
    name = "alpha"

p=Proton(momentum=10)
p.print_info()
a=Alpha(momentum=5)
a.print_info()