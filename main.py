import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from vk_api.utils import get_random_id
import requests
import time
from timetable import timetable
from datetime import date



def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """

    vk_session = vk_api.VkApi(token='<token>') #Сюда вводим токен сообщества, с которого бот будет работать

    longpoll = VkBotLongPoll(vk_session, '<id>') #Сюда вводим ID группы

    today = date.today()

    vk = vk_session.get_api()
    session = requests.Session()

    #Upload meme
    attachments = []
    upload = VkUpload(vk_session)
    meme_url = "https://meme-api.herokuapp.com/gimme" #Сюда происходит запрос для получения url мема
    
    #Bot name
    botName = "[club163446807|@volchonok.media] " #Здесь нужно написать имя группы по которому обращаются к ней в беседе

    commands = {  #Для вызова всех команд нужно набрать "help", так же сюда нужно ввести другие команды: если необходимо
    'help'          : 'Показать все команды',
    'meme'          : 'Получить новый мем',
    'timetable'     : 'Расписание на день'
    }

    print(today)
    for event in longpoll.listen():
        print(event) #Parse VK event and JSON
        if event.type == VkBotEventType.MESSAGE_NEW:
            #Слушаем longpoll, если пришло сообщение то:
            
            print('Новое сообщение:')
            print('Для меня от: ', end='')
            print(event.message.from_id)
            print('Текст:', event.message.text)
            print()
            word = event.message.text.lower()

            if word == botName + 'meme' or word == 'meme': #Если написали meme
                if event.from_user: #Если написали в ЛС
                    attachments = []
                    response = requests.get(meme_url)
                    image_url = response.json()
                    image = session.get(image_url['url'], stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append(
                        'photo{}_{}'.format(photo['owner_id'], photo['id'])
                    )
                    vk.messages.send( #Отправляем сообщение
                        user_id=event.message.from_id,
                        random_id=get_random_id(),
                        attachment=','.join(attachments)
                    )
                elif event.from_chat: #Если написали в Беседе
                    attachments = []
                    response = requests.get(meme_url)
                    image_url = response.json()
                    image = session.get(image_url['url'], stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append(
                        'photo{}_{}'.format(photo['owner_id'], photo['id'])
                    )
                    vk.messages.send( #Отправляем собщение
                        chat_id=event.chat_id,
                        random_id=get_random_id(),
                        attachment=','.join(attachments)
                    )
            elif word == botName + 'timetable' or word == 'timetable': #Если написали timetable
                today = str(date.today())
                if event.from_user: #Если написали в ЛС
                    if today in timetable:
                        vk.messages.send( #Отправляем сообщение
                            user_id=event.message.from_id,
                            random_id=get_random_id(),
                            message=today + "\n" + timetable[today]
                        )
                    else:
                        vk.messages.send( #Отправляем сообщение
                            user_id=event.message.from_id,
                            random_id=get_random_id(),
                            message="Сегодня нет пар, спи дальше, котик <3"
                        )
                        vk.messages.send( #Отправляем сообщение
                            user_id=event.message.from_id,
                            random_id=get_random_id(),
                            sticker_id="11280" #id stiker
                        )
                if event.from_chat:#Если написали в Беседе
                    if today in timetable:
                        vk.messages.send( #Отправляем сообщение
                            chat_id=event.chat_id, #Здесь chat_id
                            random_id=get_random_id(),
                            message=today + "\n" + timetable[today]
                        )
                    else:
                        vk.messages.send( #Отправляем сообщение
                            chat_id=event.chat_id, #Здесь chat_id
                            random_id=get_random_id(),
                            message="Сегодня нет пар, спи дальше, котик <3"
                        )
                        vk.messages.send( #Отправляем сообщение
                            chat_id=event.chat_id, #Здесь chat_id
                            random_id=get_random_id(),
                            sticker_id="11280" #id stiker
                        )
            elif word == botName + 'help' or word == 'help' or word == botName + 'start' or word == 'start': #Если написали help or start
                if event.from_user: #Если написали в ЛС
                    help_text = "Доступные команды: \n"
                    for key in commands:  #Генерируем вывод комманд при запросе help
                        help_text += key + " - "
                        help_text += commands[key] + "\n"
                    vk.messages.send( #Отправляем сообщение
                        user_id=event.message.from_id,
                        random_id=get_random_id(),
                        message=help_text
                    )
                elif event.from_chat:#Если написали в Беседе
                    help_text = "Доступные команды: \n"
                    for key in commands:  #Генерируем вывод комманд при запросе help
                        help_text += key + " - "
                        help_text += commands[key] + "\n"
                    vk.messages.send( #Отправляем сообщение
                        chat_id=event.chat_id, #Здесь chat_id
                        random_id=get_random_id(),
                        message=help_text
                    )
            else: #Если пришло не известное сообщение
                if event.from_user: #Если написали в ЛС
                    vk.messages.send( #Отправляем сообщение
                        user_id=event.message.from_id,
                        random_id=get_random_id(),
                        message="Такой нет команды"
                    )
                    vk.messages.send( #Отправляем сообщение
                            user_id=event.message.from_id,
                            random_id=get_random_id(),
                            sticker_id="7227" #id stiker
                    )
                if event.from_chat:#Если написали в Беседе
                    vk.messages.send( #Отправляем сообщение
                        chat_id=event.chat_id,
                        random_id=get_random_id(),
                        message="Такой нет команды"
                    )
                    vk.messages.send( #Отправляем сообщение
                            chat_id=event.chat_id, #Здесь chat_id
                            random_id=get_random_id(),
                            sticker_id="7227" #id stiker
                    )
    print()


if __name__ == '__main__':
    main()
