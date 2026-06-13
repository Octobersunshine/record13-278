import random
import secrets
import warnings
from typing import List, Optional, Union


class RandomService:
    def __init__(self, seed: Optional[int] = None, secure: bool = True):
        self.secure = secure
        self._rng: Optional[random.Random] = None
        if secure:
            if seed is not None:
                warnings.warn(
                    "Seed is ignored when secure=True (CSPRNG does not support seeding).",
                    UserWarning,
                    stacklevel=2,
                )
        else:
            self._rng = random.Random(seed)

    def _secure_randint(self, low: int, high: int) -> int:
        return low + secrets.randbelow(high - low + 1)

    def _secure_uniform(self, low: float, high: float) -> float:
        bits = secrets.randbelow(2 ** 53)
        normalized = bits / (2 ** 53)
        return low + normalized * (high - low)

    def randint(self, low: int, high: int) -> int:
        if low > high:
            low, high = high, low
        if self.secure:
            return self._secure_randint(low, high)
        return self._rng.randint(low, high)

    def uniform(self, low: float, high: float) -> float:
        if low > high:
            low, high = high, low
        if self.secure:
            return self._secure_uniform(low, high)
        return self._rng.uniform(low, high)

    def randrange(self, start: int, stop: Optional[int] = None, step: int = 1) -> int:
        if step == 0:
            raise ValueError("step argument must not be zero")
        if stop is None:
            start, stop = 0, start
        total_steps = (stop - start + step - (1 if step > 0 else -1)) // step
        if total_steps <= 0:
            raise ValueError("empty range for randrange()")
        if self.secure:
            idx = secrets.randbelow(total_steps)
            return start + idx * step
        return self._rng.randrange(start, stop, step)

    def choice(self, seq: List[Union[int, float, str]]) -> Union[int, float, str]:
        if not seq:
            raise ValueError("Cannot choose from an empty sequence")
        if self.secure:
            idx = secrets.randbelow(len(seq))
            return seq[idx]
        return self._rng.choice(seq)

    def sample(self, population: List[Union[int, float, str]], k: int) -> List[Union[int, float, str]]:
        if k < 0:
            raise ValueError("Sample larger than population or is negative")
        if k > len(population):
            raise ValueError("Sample larger than population or is negative")
        if self.secure:
            result: List[Union[int, float, str]] = []
            selected: List[int] = []
            n = len(population)
            while len(selected) < k:
                idx = secrets.randbelow(n)
                if idx not in selected:
                    selected.append(idx)
                    result.append(population[idx])
            return result
        return self._rng.sample(population, k)

    def shuffle(self, seq: List[Union[int, float, str]]) -> List[Union[int, float, str]]:
        shuffled = seq.copy()
        n = len(shuffled)
        if self.secure:
            for i in range(n - 1, 0, -1):
                j = secrets.randbelow(i + 1)
                shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        else:
            self._rng.shuffle(shuffled)
        return shuffled

    def randints(self, low: int, high: int, count: int) -> List[int]:
        if count < 0:
            raise ValueError("Count cannot be negative")
        return [self.randint(low, high) for _ in range(count)]

    def uniforms(self, low: float, high: float, count: int) -> List[float]:
        if count < 0:
            raise ValueError("Count cannot be negative")
        return [self.uniform(low, high) for _ in range(count)]
