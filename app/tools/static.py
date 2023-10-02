from enum import Enum


class Fuel(Enum):
    GAS = 'gas'
    KEROSENE = 'kerosine'
    WIND = 'wind'


class PowerPlant:
    GAS = 'gasfired'
    KEROSENE = 'turbojet'
    WIND = 'windturbine'


class FuelPrice:
    GAS = 'gas(euro/MWh)'
    KEROSENE = 'kerosine(euro/MWh)'


class WindPercentageAvailable:
    PERCENTAGE = 'wind(%)'