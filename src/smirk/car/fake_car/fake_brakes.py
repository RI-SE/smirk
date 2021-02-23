from smirk.car.brakes import Brakes


class FakeBrakes(Brakes):
    def brake(self):
        print("Braking!")
