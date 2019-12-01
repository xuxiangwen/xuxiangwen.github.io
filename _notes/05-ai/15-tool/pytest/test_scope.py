import pytest
@pytest.fixture(scope='function')
def func_scope():
    pass


@pytest.fixture(scope='module')
def mod_scope():
    pass


@pytest.fixture(scope='session')
def sess_scope():
    pass


@pytest.fixture(scope='class')
def class_scope():
    pass
    
@pytest.mark.usefixtures('class_scope')
class TestClassScope:
    def test_1(self):
        pass

    def test_2(self):
        pass    

def test_multi_scope(sess_scope, mod_scope, class_scope, func_scope):
    pass
    
def test_multi_scope1(sess_scope, mod_scope, class_scope, func_scope):
    pass    
