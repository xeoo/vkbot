import vk_api
from components import functions, handler
from vk_api.bot_longpoll import VkBotLongPoll

config = functions.load_json()
vk_session = vk_api.VkApi(token=config["token"])
longpoll = VkBotLongPoll(vk_session, config["group_id"])
api = vk_session.get_api()

bot = handler.Bot(api, longpoll, config)
bot.start_bot()
