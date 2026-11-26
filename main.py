import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

TEXTS = {
    "ru": {
        "start": "Привет! ✨ Я — Мультик Магия!\nСделаю персональный мультфильм о том, кого ты любишь ❤️\nДля кого делаем мультик?",
        "occasion": "Супер! А какой повод?",
        "heroes": "Как зовут героя — и кто ещё должен быть в мультике?\nПитомцев тоже пиши с кличками 😊\nНапример: София, кот Барсик и собака Боня",
        "age": "Сколько лет герою?",
        "photo": "Отлично! А теперь пришли фото героя 📸\nЧем лучше видно личико, тем больше герой будет похож!",
        "story": "Почти готово! Расскажи в 2-х словах, про что мультик?\nНапример: «София спасает кота от дракона»",
        "voice": "Кто рассказывает сказку?",
        "music": "А какая музыка?",
        "wait": "Волшебство началось... ✨ Делаю твоего героя... 20 секунд...",
        "final": "Вот твой герой! Правда похож? 😍\n\nХочешь из этого настоящий мультик на 30 секунд — со сказкой, голосом и музыкой?\nЭто будет твой личный мультик, такого ни у кого нет!",
        "want_cartoon": "🎬 Хочу мультик — 150 ⭐"
    },
    "en": {
        "start": "Hi! ✨ I'm Multik Magic!\nI'll make a personal cartoon about someone you love ❤️\nWho is it for?",
        "occasion": "Great! What's the occasion?",
        "heroes": "What's the hero's name — and who else should be in the cartoon?\nPets too, with nicknames 😊\nFor example: Sofia, cat Barsik and dog Bonya",
        "age": "How old is the hero?",
        "photo": "Great! Now send the hero's photo 📸\nThe clearer the face, the more similar the hero will be!",
        "story": "Almost done! Tell me in a few words, what's the cartoon about?\nFor example: «Sofia saves the cat from a dragon»",
        "voice": "Who narrates the story?",
        "music": "And what music?",
        "wait": "Magic is starting... ✨ Making your hero... 20 seconds...",
        "final": "Here is your hero! Looks similar? 😍\n\nWant a real 30-second cartoon from this — with a story, voice and music?\nIt will be your personal cartoon, no one else has it!",
        "want_cartoon": "🎬 I want a cartoon — 150 ⭐"
    }
}

class Form(StatesGroup):
    lang = State()
    for_whom = State()
    occasion = State()
    heroes = State()
    age = State()
    photo = State()
    story = State()
    voice = State()
    music = State()

def lang_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])

def kb_for(lang, buttons):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t, callback_data=c) for t,c in row] for row in buttons])

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! / Hello! ✨\nВыбери язык / Choose language:", reply_markup=lang_kb())
    await state.set_state(Form.lang)

@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(call: types.CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    await state.update_data(lang=lang)
    t = TEXTS[lang]
    if lang == "ru":
        kb = kb_for(lang, [[("🎁 В подарок","for_gift"),("💖 Для себя","for_self")],[("👨‍👩‍👧 Для семьи","for_family")]])
    else:
        kb = kb_for(lang, [[("🎁 As a gift","for_gift"),("💖 For myself","for_self")],[("👨‍👩‍👧 For family","for_family")]])
    await call.message.answer(t["start"], reply_markup=kb)
    await state.set_state(Form.for_whom)
    await call.answer()

@dp.callback_query(F.data.startswith("for_"))
async def for_whom(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    t = TEXTS[lang]
    if lang == "ru":
        kb = kb_for(l
   ang, [[("🎂 День рождения","occ_birthday")],[("🎄 Праздник","occ_holiday")],[("✨ Просто так","occ_just")]])
    else:
        kb = kb_for(lang, [[("🎂 Birthday","occ_birthday")],[("🎄 Holiday","occ_holiday")],[("✨ Just for fun","occ_just")]])
    await call.message.answer(t["occasion"], reply_markup=kb)
    await state.set_state(Form.occasion)
    await call.answer()

@dp.callback_query(F.data.startswith("occ_"))
async def occasion(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    await call.message.answer(TEXTS[lang]["heroes"])
    await state.set_state(Form.heroes)
    await call.answer()

@dp.message(Form.heroes)
async def heroes(message: types.Message, state: FSMContext):
    await state.update_data(heroes=message.text)
    data = await state.get_data()
    lang = data["lang"]
    if lang == "ru":
        kb = kb_for(lang, [[("0-3 года","age_0"),("4-6 лет","age_4")],[("7-12 лет","age_7"),("13+","age_13")]])
    else:
        kb = kb_for(lang, [[("0-3 years","age_0"),("4-6 years","age_4")],[("7-12 years","age_7"),("13+","age_13")]])
    await message.answer(TEXTS[lang]["age"], reply_markup=kb)
    await state.set_state(Form.age)

@dp.callback_query(F.data.startswith("age_"))
async def age(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    await call.message.answer(TEXTS[lang]["photo"])
    await state.set_state(Form.photo)
    await call.answer()

@dp.message(Form.photo, F.photo)
async def photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    data = await state.get_data()
    lang = data["lang"]
    await message.answer(TEXTS[lang]["story"])
    await state.set_state(Form.story)

@dp.message(Form.story)
async def story(message: types.Message, state: FSMContext):
    await state.update_data(story=message.text)
    data = await state.get_data()
    lang = data["lang"]
    if lang == "ru":
        kb = kb_for(lang, [[("👩 Женский","voice_f"),("👨 Мужской","voice_m")],[("🧒 Детский","voice_k")]])
    else:
        kb = kb_for(lang, [[("👩 Female","voice_f"),("👨 Male","voice_m")],[("🧒 Child","voice_k")]])
    await message.answer(TEXTS[lang]["voice"], reply_markup=kb)
    await state.set_state(Form.voice)

@dp.callback_query(F.data.startswith("voice_"))
async def voice(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    if lang == "ru":
        kb = kb_for(lang, [[("🎵 Весёлая","mus_happy")],[("🌙 Спокойная","mus_calm")],[("✨ Волшебная","mus_magic")]])
    else:
        kb = kb_for(lang, [[("🎵 Happy","mus_happy")],[("🌙 Calm","mus_calm")],[("✨ Magical","mus_magic")]])
    await call.message.answer(TEXTS[lang]["music"], reply_markup=kb)
    await state.set_state(Form.music)
    await call.answer()

@dp.callback_query(F.data.startswith("mus_"))
async def music(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data["lang"]
    t = TEXTS[lang]
    await call.message.answer(t["wait"])
    await call.message.answer_photo(photo=data["photo_id"], caption=t["final"], reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t["want_cartoon"], callback_data="buy")]]))
    await state.clear()
    await call.answer()

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())                 
