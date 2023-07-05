from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from keyboards.common import cb, main_ikb
from keyboards.cats import cat_ikb
from modules.cats import get_cat_photo
from states.common import ProfileStatesGroup
from aiogram.types import InputFile
from aiogram.utils.exceptions import MessageCantBeDeleted


# Котики
# @dp.callback_query_handler(cb.filter(), state='*')
async def cb_cat(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    popup_text = "Вскоре на экране появится очаровательный котик"
    if callback.data == "ikb:cat":
        await ProfileStatesGroup.cat.set()
        try:
            await callback.answer(text=popup_text)
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            # await callback.message.delete()
            await bot.send_photo(chat_id=callback.message.chat.id, photo=InputFile.from_url(get_cat_photo()), reply_markup=cat_ikb())
        except MessageCantBeDeleted:
            await bot.send_message(chat_id=callback.message.chat.id, text="Попробуйте снова", reply_markup=main_ikb())

    elif callback.data == "ikb:cat_photo":
        await ProfileStatesGroup.cat.set()
        # print(await state.get_state())
        await callback.answer(text=popup_text)
        await callback.message.edit_media(types.InputMedia(media=InputFile.from_url(get_cat_photo()),
                                                           type='photo'),
                                                           reply_markup=cat_ikb())
        

def register_handlers_cats(dp: dp):
    dp.register_callback_query_handler(cb_cat, cb.filter(), state='*')