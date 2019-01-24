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
        self._issuer = issuer
        self._time = time
        self._date = date
        self._source_energy = source_energy
        self._identity = identity
        self._capacity = capacity
        self._commissioning_date = commissioning_date
        self._loc_of_gen = loc_of_gen
        self._units = units
        self._other_options = other_options

    #issuer
    @property
    def issuer(self):
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        self._issuer = issuer

    @issuer.deleter
    def issuer(self):
        pass

    #time
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time

    @time.deleter
    def time(self):
        pass

    #date
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @date.deleter
    def date(self):
        pass

    #source_energy
    @property
    def source_energy(self):
        return self._source_energy

    @source_energy.setter
    def source_energy(self, source_energy):
        self._source_energy = source_energy

    @source_energy.deleter
    def source_energy(self):
        pass

    #identity
    @property
    def identity(self):
        return self._identity

    @identity.setter
    def identity(self, identity):
        self._identity = identity

    @identity.deleter
    def identity(self):
        pass

    #capacity
    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        self._capacity = capacity

    @capacity.deleter
    def capacity(self):
        pass

    #commissioning_date
    @property
    def commissioning_date(self):
        return self._commissioning_date

    @commissioning_date.setter
    def commissioning_date(self, commissioning_date):
        self._commissioning_date = commissioning_date

    @commissioning_date.deleter
    def commissioning_date(self):
        pass

    #loc_of_gen
    @property
    def loc_of_gen(self):
        return self._loc_of_gen

    @loc_of_gen.setter
    def loc_of_gen(self, loc_of_gen):
        self._loc_of_gen = loc_of_gen

    @loc_of_gen.deleter
    def loc_of_gen(self):
        pass

    #units
    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units):
        self._units = units

    @units.deleter
    def units(self):
        pass

    #other_options
    @property
    def other_options(self):
        return self._other_options

    @other_options.setter
    def other_options(self, other_options):
        self._other_options = other_options

    @other_options.deleter
    def other_options(self):
        pass

    def __str__(self):
        return "Issuer: " + self._issuer + " Time: " + self._time + " Date: " + self._date + " Source: " + \
               self._source_energy + " Identity: " + self._identity + " Capacity: " + self._capacity + \
               " Commision date:" + self._commissioning_date + " Location of gen: " + self._loc_of_gen + \
                " Units: " + self._units + " Other Options: " + self._other_options + "\n"

    def __repr__(self):
        return "Issuer: " + self._issuer + " Time: " + self._time + " Date: " + self._date + " Source: " + \
               self._source_energy + " Identity: " + self._identity + " Capacity: " + self._capacity + \
               " Commision date:" + self._commissioning_date + " Location of gen: " + self._loc_of_gen + \
                " Units: " + self._units + " Other Options: " + self._other_options + "\n"

    def create_json(self):
        cert = dict()
        cert["issuer"] = self._issuer
        cert["time"] = self._time
        cert["data"] = self._date
        cert["source_energy"] = self.source_energy
        cert["identity"] = self._identity
        cert["capacity"] = self._capacity
        cert["commissioning_date"] = self._commissioning_date
        cert["loc_of_gen"] = self._loc_of_gen
        cert["units"] = self._units
        cert["other_options"] = self._other_options
        return cert


