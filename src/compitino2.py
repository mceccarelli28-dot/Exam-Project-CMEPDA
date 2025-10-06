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
#Definiamo inizialmente la classe base da cui poi erediteranno le child proton ed alpha
class Particle:
    #nell'init definiamo solo gli attributi tra quelli definiti nella richiesta sul costruttore della classe, ovviamente inizializziamo siano nulli
    def __init__(self, *, energy=None, momentum=None, beta=None, gamma=None):
        """
        Inizializziamo con carica, massa e nome, ma le definiamo in seguito con le properties, sia per poterle chiamare con l'operatore dot come richiesto, sia perchè è necessario per definirli come attributi di classe child
        """
        # Questo comando permette di sapere quante quantità vengono inizializzate, se sono più di una da errore (mi conta il numero di variabili con un for e sommando su queste)
        quantities = [energy, momentum, beta, gamma]
        if sum(q is not None for q in quantities) > 1:
            raise ValueError("Set only one quantity among energy, momentum, beta, gamma.")

        # Settiamo il valore del momento inizializzato a 0
        self._momentum = 0.0

        # Inizializza la quantità scelta, ossia quella che quando si chiama una certa classe child non sia a 0, per esempio in p=Proton(momentum=40) si avrà solo il momento e le altre nulle, attraverso ciclo if ed elif
        if momentum is not None:
            self.momentum = momentum
        elif energy is not None:
            self.energy = energy
        elif beta is not None:
            self.beta = beta
        elif gamma is not None:
            self.gamma = gamma
        # Se nessuna quantità è passata, momentum = 0

    # definiamo le quantità da inizializzare come attributi di classe con le properties e il comando self.__class__, cosicchè quando vengono chiamate, si ha self.Proton.mass che richiama all'attributo di classe.
    @property
    def mass(self):
        return self.__class__.mass

    @property
    def charge(self):
        return self.__class__.charge

    @property
    def name(self):
        return self.__class__.name

    #Definiamo le property delle altre quantità, in modo tale che vengano calcolate quando non inizializzate 
    @property
    def energy(self):
        return math.sqrt(self._momentum**2 + self.mass**2)
    #il setter è necessario sia per valutare se il valore sia fisico, sia perchè permette di aggiornare il momento quando si sceglie di inizializzare una quantità diversa da quello
    @energy.setter
    def energy(self, E):
        if E < self.mass:
            raise ValueError("Energy must be >= rest mass.")
        self._momentum = math.sqrt(E**2 - self.mass**2)
    
    @property
    def momentum(self):
        return self._momentum

    @momentum.setter
    def momentum(self, p):
        if p < 0:
            raise ValueError("Momentum cannot be negative.")
        self._momentum = p
    
    @property
    def beta(self):
        return self._momentum / self.energy

    @beta.setter
    def beta(self, b):
        if not (0 <= b < 1):
            raise ValueError("Beta must be between 0 and 1.")
        gamma = 1 / math.sqrt(1 - b**2)
        self._momentum = self.mass * b * gamma

   
    @property
    def gamma(self):
        return self.energy / self.mass

    @gamma.setter
    def gamma(self, g):
        if g < 1:
            raise ValueError("Gamma must be >= 1")
        self._momentum = self.mass * math.sqrt(g**2 - 1)

    #si definisce un comando che permette di dare una lista delle quantità richieste con loguru
    def print_info(self):
        logger.info(f"Particle: {self.name}")
        logger.info(f"  Mass     : {self.mass:.3f} MeV/c²")
        logger.info(f"  Charge   : {self.charge:+} e")
        logger.info(f"  Momentum : {self.momentum:.3f} MeV/c")
        logger.info(f"  Energy   : {self.energy:.3f} MeV")
        logger.info(f"  Beta     : {self.beta:.5f}")
        logger.info(f"  Gamma    : {self.gamma:.5f}")

#definiamo le child class con gli attributi di classe come richiesto
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