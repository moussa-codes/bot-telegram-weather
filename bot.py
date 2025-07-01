import os 
from dotenv import load_dotenv
from telegram.ext import CommandHandler, ApplicationBuilder
import requests

load_dotenv()
TOKEN=os.getenv('TOKEN')
KEY=os.getenv("API_KEY")

async def start(update,context):
    await update.message.reply_text("Salut et bienvenue ! Utilise /weather Ville pour connaître la météo.")

async def weather(update,context):
    if len(context.args) == 0:
        await update.message.reply_text("Utilise comme ça : /weather Ville")
        return
     
    ville="".join(context.args)
    meteo= await get_weather(ville)
    await update.message.reply_text(meteo)

async def get_weather(ville):
    url=f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={KEY}&units=metric&lang=fr"
    response=requests.get(url)

    if response.status_code==200:
        data=response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Météo à {ville} : {temp}°C, {desc}"
    else:
        return "Ville introuvable ou erreur d'API"

async def help(update,context):
    await update.message.reply_text("/start -Démarrer le bot\n/wheather Ville -Obtenir la météo\n/help -Afficher l'aide (tu viens de le faire...)") 

app=ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("weather",weather))
app.add_handler(CommandHandler("help",help))

app.run_polling(poll_interval=5)



