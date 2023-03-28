from discord.ext import tasks

import discord
import credentials
import moodle_interaction
from datetime import datetime as dt
from datetime import date
import time

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=60)  # task runs every minute
    async def my_background_task(self):
        current_time = dt.now()

        time_to_compare = "01:22"

        hour_to_compare, minute_to_compare = map(int, time_to_compare.split(':'))

        if current_time.hour == hour_to_compare and current_time.minute == minute_to_compare:
            channel = self.get_channel(credentials.CHANNEL_ID)

            message = ""

            username = credentials.USERNAME
            password = credentials.PASSWORD
            session = moodle_interaction.login_moodle(username, password)
            activities_today = moodle_interaction.get_activities(session)
            # activities_tomorrow = moodle_interaction.get_activities(session, dt.today().day + 1)

            if activities_today:
                message += "@everyone \n**Atenção!!** As seguintes atividades serão fechadas **hoje**:\n"
                for dict in activities_today:
                    message += "    • **Atividade:** " + dict['activity'] + "\n        → **Disciplina:** " + dict['course'] + "\n"
            else:
                message += "Nenhuma atividade será fechada hoje\n"

            # EM CONSTRUÇÃO
            # if activities_tomorrow:
            #     if(len(message) == 0):
            #         message += "@everyone Bom dia! "
            #     message += "As seguintes atividades serão fechadas amanhã:\n"
            #     for activity in activities_tomorrow:
            #         message += activity + "\n"
            # else:
            #     message += "Nenhuma atividade será fechada amanhã"

            await channel.send(message)
            

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(credentials.TOKEN)