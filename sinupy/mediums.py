"""Medium Class & The Classes Derived from It

Author: Wenyin Wei wenyin.wei@ipp.ac.cn

"""

class Medium:
    def __init__(self, name="Unknown Medium"):
        if name: self.name = name


class Plasma(Medium): 
    def __init__(self, name="Plasma"):
        super().__init__(name=name)


class MaxwellPlasma(Plasma):
    def __init__(self, name="Maxwell Plasma"):
        super().__init__(name=name)