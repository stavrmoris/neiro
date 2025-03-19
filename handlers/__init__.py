from aiogram import Dispatcher, Router
from . import (start, neiro, models, sub)


def register_routers(rt: Router):
    start.router(rt)
    neiro.router(rt)
    models.router(rt)
    sub.router(rt)
