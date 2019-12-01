import pytest

class Generator():
    def __init__(self, version='0.1.0'):
        self.__version__ = version
    def unique_id(self):
        return 1
        
gen = Generator('0.1.0')

@pytest.mark.xfail(gen.__version__ < '0.2.0',
                   reason='not supported until v0.2.0')
def test_api():
    id_1 = gen.unique_id()
    id_2 = gen.unique_id()
    assert id_1 != id_2

def test_api1():
    id_1 = gen.unique_id()
    id_2 = gen.unique_id()
    assert id_1 == id_2
    
