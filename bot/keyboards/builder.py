from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def default_keyboard_builder(message, keyboards, column_name='name'):
    keyboard_buttons = []
    
    row = []
    for item in keyboards:
        button_text = getattr(item, column_name)
        row.append(KeyboardButton(text=button_text))
        
        if len(row) == 2:
            keyboard_buttons.append(row)
            row = []
    
    if row:
        keyboard_buttons.append(row)
    
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=keyboard_buttons
    )
    
    return keyboard