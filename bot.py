from discord.ext import tasks

import discord
import credentials
import moodle_interaction
from datetime import datetime as dt
from datetime import date
import time
from days import day

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

        time_to_compare = "13:00"

        hour_to_compare, minute_to_compare = map(int, time_to_compare.split(':'))

        if current_time.hour == hour_to_compare and current_time.minute == minute_to_compare:
            channel = self.get_channel(credentials.CHANNEL_ID)

            message = ""

            username = credentials.USERNAME
            password = credentials.PASSWORD
            session = moodle_interaction.login_moodle(username, password)

            weekday = dt.today().weekday()
            activities_today = moodle_interaction.get_activities(session)
            activities_tomorrow = moodle_interaction.get_activities(session, day.AMANHA)

            if activities_today or activities_tomorrow or weekday == 4:
                message += "@everyone Bom dia!\n"

            if activities_today:
                message += "**Atenção!!** As seguintes atividades serão fechadas **hoje**:\n"
                for dict in activities_today:
                    message += "    • **Atividade:** " + dict['activity'] + "\n        → **Disciplina:** " + dict['course'] + "\n"
            else:
                message += "Nenhuma atividade será fechada hoje\n"

            message += "------------------------------------------------\n"

            if activities_tomorrow:
                message += "As seguintes atividades serão fechadas **amanhã:**\n"
                for dict in activities_tomorrow:
                    message += "    • **Atividade:** " + dict['activity'] + "\n        → **Disciplina:** " + dict['course'] + "\n"
            else:
                message += "Nenhuma atividade será fechada amanhã\n"

            if weekday == 4:
                all_activities = moodle_interaction.get_all_activities(session)
                message += "------------------------------------------------\n"
                message += "SEXTOU! Vai descansar. Mas se quiser adiantar as próximas atividades, elas são as seguintes:\n"
                for dict in all_activities:
                    message += "    • **Atividade:** " + dict['activity'] + "\n        → **Disciplina:** " + dict['course'] + "\n        → **Término:** " + dict['date'] + "\n"

            await channel.send(message)
            

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(credentials.TOKEN)