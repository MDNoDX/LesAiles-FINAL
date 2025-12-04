from aiogram.fsm.state import StatesGroup, State

class OrderState(StatesGroup):
    order_type = State()
    location = State()
    branch_selection = State()
    category = State()
    product = State()
    quantity = State()
    cart = State()
    payment = State()
    contact = State()
    comment = State()
    confirmation = State()