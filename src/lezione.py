import math


class Particle:
    def __init__(self, mass, charge, name, momentum=0.):
        self._mass=mass
        self._charge=charge
        self._name=name
        self.momentum=momentum #essendo una variabile che posso settare, la mantengo tra gli attributi pubblici e poi uso il setter per inizializzarla

    @property
    def mass(self):
         return self._mass
    @property
    def charge(self):
         return self._charge
    @property
    def name(self):
         return self._name
    @property
    def momentum(self):
         return self._momentum
    
    @momentum.setter
    def momentum(self,momentum):
        if momentum < 0:
              print('nun se fa')
              print('the momentum is 0')
              self._momentum=0 #sto inizializzando il momentum nel setter con l'attributo privato
        else:
             self._momentum=momentum

         

    @property
    def energy(self):
        return math.sqrt(self.mass**2 + self.momentum**2)
    @energy.setter
    def energy(self,energy):
        if energy<self.mass:
            print('sucm o pesc')
        else: 
            self.momentum = math.sqrt(energy**2-self.mass**2)

    @property
    def beta(self):
         return self.momentum/self.energy
    
    @beta.setter
    def beta(self,beta):
        if (beta < 0) or (beta > 1):
              print('ricchio')
        elif beta>=1 and self.mass<=0:
             print('non funzia')
        else:
             self.momentum = beta * self.energy
    
    

    def print_info(self):
        print(f'Particle {self.name} of mass {self.mass} MeV and charge {self.charge} e')
        print(f'The particle momentum  is {self.momentum} MeV')


class Proton(Particle):
     MASS = 938.1
     CHARGE = 1
     NAME = 'Proton'
     def __init__(self,momentum=0.):
          Particle.__init__(self, mass = self.MASS, charge = self.CHARGE, name = self.NAME ,momentum = momentum) #potrei anche usare Proton.MASS, scelta estetica
          


if __name__ == '__main__':
        muon = Particle(mass=104.6, charge=-1, name='Muon',momentum=10)
        print(muon.energy)
        muon.momentum=-10
        muon.energy=200
        muon.print_info()
        p=Proton()
        p.print_info()
    


