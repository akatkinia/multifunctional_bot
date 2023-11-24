import pytest


@pytest.fixture
def fsm_context(mocker):
    def _f(state=None):
        async def get_state():
            return state
        fsm = mocker.AsyncMock()
        fsm.get_state = get_state
        return fsm
    return _f


@pytest.fixture
def bot_cb(mocker):
    return mocker.AsyncMock()
