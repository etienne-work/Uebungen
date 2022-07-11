###############################
# Ober-/ Superklasse Fahrzeug #
###############################


class Vehicle(object):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    # Wert VehicleInfoGruppe (dict) oder None zurückgeben #
    # Lichtgeschwindigkeit Standard ober- & Untergrenz #
    def __init__(
        self,
        name: str,
        maxSpeed: int = 299792,
        minSpeed: int = -299792,
        seats: dict = {},
        maxSeats: int = 0,
    ) -> None:
        if maxSeats < 0:
            maxSeats = 0
        self._vehicleInfo = {
            "name": name,
            "speed": {  # geschwindigkeit Info Fahrzeug
                "currSpeed": 0,
                "maxSpeed": maxSpeed,
                "minSpeed": minSpeed,
            },
            "seats": {  # besetzte sitze Information
                "driver": False,  # True -> am Steuer/False -> nicht am Steuer/None -> kein Fahrersitz
                "passenger": seats,
                "maxSeats": maxSeats,  # maximale Anzahl Sitze (seats können entfernt & hinzugefügt werden)
            },
        }

    # Wert aus vehicleInfoGruppe (str/int) oder None zurückgeben #
    def getVehicleInfo(self):
        return self._vehicleInfo

    def getVehicleInfoByNames(self, infoIndex: str = None, groupNames: str | list[str] = []):
        vehicleInfo = self.getVehicleInfo()
        if type(groupNames) == str:
            groupNames = [groupNames]
        if groupNames is not None:
            for group in groupNames:
                if group is not None:
                    if group in vehicleInfo:
                        vehicleInfo = vehicleInfo[group]
        if infoIndex is not None:
            if infoIndex in vehicleInfo:
                return vehicleInfo[infoIndex]
            else:
                return self.getVehicleInfoByIndex(infoIndex)
        return vehicleInfo

    def getVehicleInfoByIndex(self, infoIndex: str | None):
        if infoIndex is not None and type(infoIndex) is not int:
            for key, info in self.getVehicleInfo().items():
                if key == infoIndex:
                    return info
                elif infoIndex in info:
                    return info[infoIndex]
        return None

    def setVehicleInfo(self, newVehicleInfo: dict) -> None:
        self._vehicleInfo = newVehicleInfo

    # Update Fahrzeuginfo #
    def setVehicleInfoByNames(
        self,
        newInfo: str | int | dict = None,
        infoIndex: str | int = None,
        groupNames: str | list[str] = None,
    ) -> bool:
        vehicleInfo = (
            lambda res: res if (res is not None and res is not False) else self.getVehicleInfo()
        )(self.getVehicleInfoByNames(groupNames=groupNames))
        vehicleInfo[infoIndex] = newInfo

    # installation eines Sitzes #
    def addSeat(self, seat: int | str = 1) -> bool:
        if seat is not None:
            seats = self.getVehicleInfoByNames("seats")
            if seat not in seats:
                if len(seats["passenger"]) + 1 <= seats["maxSeats"]:
                    self.setVehicleInfoByNames(
                        False,
                        groupNames=["seats", "passenger"],
                        infoIndex=seat,
                    )
                    return True
        return False

    # Enteferne Sitz aus Auto#
    def removeSeat(self, seat: str | int) -> bool:
        if seat is not None:
            seats = self.getVehicleInfoByNames(groupNames="seats", infoIndex="passenger")
            if seat in seats:
                seats.pop(seat)
                return True
        return False

    # an Platz setzen (wenn Sitz vorhanden, nicht besetzt & Auto still) #
    def occupySeat(self, seatType: str = "driver", seat: int | str = 1) -> bool:
        seatInfo = self.getVehicleInfoByNames(groupNames=["seats", "passenger"], infoIndex=seat)
        if not self.isParked():
            print("Es ist nicht sicher, in ein Fahrendes Auto einzusteigen!")
            return False
        match (seatType.lower()):
            case "driver":
                if seatInfo is False:
                    self.setVehicleInfoByNames(newInfo=True, groupNames="seats", infoIndex="driver")
                    return True
            case "passenger":
                if seatInfo is not None:
                    self.setVehicleInfoByNames(
                        newInfo=True, groupNames=["seats", "passenger"], infoIndex=seat
                    )
                    return True
        print("Sitz nicht vorhanden!")
        return False

    # Platz verlassen (wenn existiert & besetzt) #
    def leaveSeat(self, seat: str | int = "driver") -> bool:
        if self.getVehicleInfoByNames(infoIndex=seat, groupNames="seats") and self.isParked():
            self.setVehicleInfoByNames(False, "seats", "passenger", infoIndex=seat)
            return True
        print("Es ist nicht sicher, aus einem Fahrenden Auto auszusteigen!")
        return False

    # setze Geschwindigkeit (goal) #
    def drive(self, goal: int = 50) -> bool:
        speedInfo = self.getVehicleInfoByIndex("speed")
        if self.getVehicleInfoByNames(groupNames=["driver", "seats"]):
            if goal <= speedInfo["maxSpeed"] and goal >= speedInfo["minSpeed"]:
                self.setVehicleInfoByNames(newInfo=goal, groupNames="speed", infoIndex="currSpeed")
                return True
        return False

    # Überprüfung Fahrzeug still #
    def isParked(self) -> bool:
        if self.getVehicleInfoByNames(groupNames="speed", infoIndex="currSpeed") == 0:
            return True
        return False

    @staticmethod
    # Überprüfung ob werte in Liste Leer (None) #
    def hasNoneVals(
        *varsToCheck,
    ) -> bool:  # *varscheck nimmt alle Argumente auf und speichert als tuple (array)
        for val in varsToCheck:
            if val is None:
                return True
        return False

    # Formattierung der Information und Rückgabe (bei Instanzaufruf (print))#
    def __str__(self) -> str:
        formattedText = ""
        for key, info in self.getVehicleInfo().items():
            formattedText += f"{key}: {info}\n"
        return formattedText


#################################
# Auto erbt von Klasse Fahrzeug #
#################################
class Car(Vehicle):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(
        self,
        name: str,
        maxSpeed: int = 300,
        minSpeed: int = -40,
        seats: dict = {},
        maxSeats: int = 5,
    ) -> None:
        self._isOn = False
        super().__init__(
            name=name, maxSpeed=maxSpeed, minSpeed=minSpeed, seats=seats, maxSeats=maxSeats
        )

    def drive(self, goal: int = 50) -> bool:
        if self._isOn:
            super().drive(goal)
            return True
        print("Motor läuft nicht.")
        return False

    # Ein-/Ausschalten vom Motor #
    def turnOnOff(self) -> bool:
        self._isOn = not self._isOn
        return self._isOn


####################################
# Fahrrad erbt von Klasse Fahrzeug #
####################################
class Bicycle(Vehicle):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(
        self,
        name: str,
        maxSpeed: int = 50,
        minSpeed: int = -5,
        seats: dict = {},
        maxSeats: int = 0,
    ) -> None:
        super().__init__(
            name=name,
            maxSpeed=maxSpeed,
            minSpeed=minSpeed,
            seats=seats,
            maxSeats=maxSeats,
        )


##############################
# Testfälle / Aufruf Klassen #
##############################
vehicle = Vehicle(name="Testfahrzeug")
car1 = Car(name="4 Plätzer", maxSeats=4)
car2 = Car(name="7 Plätzer", maxSeats=7, maxSpeed=200, minSpeed=-30)  # 1 driver, 7 passenger seats
bike = Bicycle(name="Fahrrad")  # 1 driver, 5 passenger seats

for i in range(7):
    print("Sitz hinzugefügt: %s" % car1.addSeat(i + 1))
    print(
        "Sitz hinzugefügt: %s" % car2.addSeat(i + 1)
    )  # wenn Falls zurückgegeben -> Sitzmaximum erreicht

print("\nAuto 1 Testfälle:")
print(f"Sitz besetzt: {car1.occupySeat()}")
print(f"Car driving: {car1.drive(20)}")
print(f"Car is on: {car1.turnOnOff()}")
print(f"Car driving: {car1.drive(20)}")
print(f"Car is parked: {car1.isParked()}")
print(f"Car is on: {car1.turnOnOff()}")

print("\nAuto 2 Testfälle:")
print(f"Sitz besetzt: {car2.occupySeat()}")
print(f"Car is on: {car2.turnOnOff()}")
print(f"Car driving: {car2.drive(300)}")

print("\nÜberprüfung Bike:")
print(bike.occupySeat())


print("\nRückgabe aller Objekte:")
print(vehicle)
print(car1)
print(car2)
print(bike)
