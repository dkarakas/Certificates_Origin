class certificate_origin:
    def __init__(self, issuer = None, time = None, date = None, source_energy = None, identity = None,
                 capacity = None, commissioning_date = None, loc_of_gen = None, units = None, other_options = None):
        """
        :param issuer: the issuer (alphanumerical)
        :param time: time of production (00:00:00)
        :param date: date of production (00-00-0000)
        :param source_energy: how the energy was produced (for now just solar)
        :param identity: TBD (for now serial_number)
        :param capacity: capacity
        :param commissioning_date: commissioning date
        :param loc_of_gen: location of the place generated the energy
        :param units: how much has been produced
        :param other_options: the purpose and eligibility of the certificate, whether public support has been
         received by the plant or the owner of the associated energy, etc.
        """
        #TODO Place checkers for the values and raise errors
        self.issuer = issuer
        self.time = time
        self.date = date
        self.source_energy = source_energy
        self.identity = identity
        self.capacity = capacity
        self.commissioning_date = commissioning_date
        self.loc_of_gen = loc_of_gen
        self.units = units
        self.other_options = other_options

        print("Empty certificated is created!")

    #issuer
    @property
    def issuer(self):
        return self.issuer

    @issuer.setter
    def issure(self, issuer):
        self.issuer = issuer

    @issuer.deleter
    def issuer(self):
        pass

    #time
    @property
    def time(self):
        return self.time

    @time.setter
    def time(self, time):
        self.time = time

    @time.deleter
    def time(self):
        pass

    #date
    @property
    def date(self):
        return self.date

    @date.setter
    def date(self, date):
        self.date = date

    @date.deleter
    def date(self):
        pass

    #source_energy
    @property
    def source_energy(self):
        return self.source_energy

    @source_energy.setter
    def source_energy(self, source_energy):
        self.source_energy = source_energy

    @source_energy.deleter
    def source_energy(self):
        pass

    #identity
    @property
    def identity(self):
        return self.identity

    @identity.setter
    def identity(self, identity):
        self.identity = identity

    @identity.deleter
    def identity(self):
        pass

    #capacity
    @property
    def capacity(self):
        return self.capacity

    @capacity.setter
    def capacity(self, capacity):
        self.capacity = capacity

    @capacity.deleter
    def capacity(self):
        pass

    #commissioning_date
    @property
    def commissioning_date(self):
        return self.commissioning_date

    @commissioning_date.setter
    def commissioning_date(self, commissioning_date):
        self.commissioning_date = commissioning_date

    @commissioning_date.deleter
    def commissioning_date(self):
        pass

    #loc_of_gen
    @property
    def loc_of_gen(self):
        return self.loc_of_gen

    @loc_of_gen.setter
    def loc_of_gen(self, loc_of_gen):
        self.loc_of_gen = loc_of_gen

    @loc_of_gen.deleter
    def loc_of_gen(self):
        pass

    #units
    @property
    def units(self):
        return self.units

    @units.setter
    def units(self, units):
        self.units = units

    @units.deleter
    def units(self):
        pass

    #other_options
    @property
    def other_options(self):
        return self.other_options

    @other_options.setter
    def isother_optionssure(self, other_options):
        self.other_options = other_options

    @other_options.deleter
    def other_options(self):
        pass