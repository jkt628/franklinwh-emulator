import random
import re
from typing import Any, override

from pydantic import BaseModel

from .unchecked import _Noise, _Stats


class APower(BaseModel):
    id: str
    ratedPwr:int= 5000
    rateBatCap:int= 13600
    modelName:str= "aPower X"


class GeneratorStats(BaseModel):
    sn: str = ""
    p_gen: float = 0
    kwh_gen: float = 0
    genStat: int = 0
    kwhGenLoad: float = 0
    genChBat: float = 0


class SmartCircuitsStats(BaseModel):
    sn: str = ""
    merged: bool = False
    pro_load: tuple[float, float, float] = (0, 0, 0)
    v2lModeEnable: int = 0
    v2lRunState: int = 0


class Noise(_Noise):
    @classmethod
    def create(cls, id: str) -> "Noise":
        # use last three digits of gateway ID for stats basis
        basis = float(id[-3:]) / 10 if re.search(r"\d{3}$", id) is not None else 1.0
        # pre-calculate 2% and .02% of the basis for noise generation
        return cls(
            basis=basis, two_percent=basis * 0.02, zero_two_percent=basis * 0.0002
        )

    def uniform2(self) -> float:
        return random.uniform(-self.two_percent, self.two_percent)

    def uniform02(self) -> float:
        return random.uniform(-self.zero_two_percent, self.zero_two_percent)

    def basis2(self) -> float:
        return self.basis + self.uniform2()

    def basis02(self) -> float:
        return self.basis + self.uniform02()


class Stats(_Stats):
    noise: Noise
    circuits: SmartCircuitsStats = SmartCircuitsStats()
    generator: GeneratorStats = GeneratorStats()

    @classmethod
    def create(cls, id: str) -> "Stats":
        return cls(noise=Noise.create(id=id), status=1)


class Gateway(BaseModel):
    id: str
    name: str
    aPower: list[APower] = []
    stats: Stats = None  # pyright: ignore[reportAssignmentType] # fix in post_init

    @override
    def model_post_init(self, context: Any) -> None:
        self.stats = Stats.create(id=self.id)

    def bump(self) -> None:
        self.stats.status += 1

    @property
    def has_circuits(self) -> bool:
        return bool(self.stats.circuits.sn)

    @property
    def has_generator(self) -> bool:
        return bool(self.stats.generator.sn)

BadGatewayError = ValueError("bad gateway")
