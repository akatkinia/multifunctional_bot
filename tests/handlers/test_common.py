import pytest

from handlers.common import cb_cancel

from keyboards.common import main_ikb


@pytest.mark.asyncio
async def test_cb_cancel_cat(fsm_context, bot_cb):
    mock_state = fsm_context('ProfileStatesGroup:cat')

    assert await cb_cancel(callback=bot_cb, state=mock_state) is None
    mock_state.finish.assert_called_once_with()
    bot_cb.message.answer.assert_called_once_with(
        text='Добро пожаловать! Снова.',
        reply_markup=main_ikb(),
    )
    bot_cb.message.delete.assert_called_once_with()


@pytest.mark.asyncio
async def test_cb_cancel_other(fsm_context, bot_cb):
    mock_state = fsm_context()

    assert await cb_cancel(callback=bot_cb, state=mock_state) is None
    mock_state.finish.assert_called_once_with()
    bot_cb.message.edit_text.assert_called_once_with(
        text='Добро пожаловать! Снова.',
        reply_markup=main_ikb(),
    )
