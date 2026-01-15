from Kamar.class_kamar import Kamar
 
class Standard(Kamar):
    def __init__(self, id_kamar):
        super().__init__(id_kamar, "Standard", 100_000)
 
class Deluxe(Kamar):
    def __init__(self, id_kamar):
        super().__init__(id_kamar, "Deluxe", 200_000)
 
class Suite(Kamar):
    def __init__(self, id_kamar):
        super().__init__(id_kamar, "Suite", 400_000)
 
class VIP(Kamar):
    def __init__(self, id_kamar):
        super().__init__(id_kamar, "VIP", 800_000)