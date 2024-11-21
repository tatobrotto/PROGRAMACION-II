
import telebot
import requests
import matplotlib.pyplot as plt
from telebot import types

# Configuración del bot y la API
TOKEN = "7731934367:AAF66mTsggvvT6PEml0q4a95_PmNkzWyfLs"
API_KEY = "137c04948e734915b5e7db2cc9da2d77"
BASE_URL = "https://api.forexrateapi.com/v1"
bot = telebot.TeleBot(TOKEN)

# Diccionario para almacenar datos temporales del usuario
user_data = {}

# Función para obtener monedas soportadas
def obtener_monedas_soportadas():
    url = f"{BASE_URL}/symbols?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        if datos.get("success"):
            return datos["symbols"]
    return None

# Función para obtener tasas actuales
def obtener_tasas_actuales(base, currencies=None):
    url = f"{BASE_URL}/latest?api_key={API_KEY}&base={base}"
    if currencies:
        url += f"&currencies={','.join(currencies)}"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        if datos.get("success"):
            return datos["rates"]
    return None

# Función para obtener tasas históricas
def obtener_tasa_historica(base, target, fecha):
    url = f"{BASE_URL}/{fecha}?api_key={API_KEY}&base={base}&currencies={target}"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        if datos.get("success"):
            return datos["rates"].get(target)
    return None

# Función para comparar tasas entre dos fechas y graficar
def comparar_tasas_y_graficar(base, target, fecha1, fecha2):
    tasa1 = obtener_tasa_historica(base, target, fecha1)
    tasa2 = obtener_tasa_historica(base, target, fecha2)

    if tasa1 is not None and tasa2 is not None:
        # Calcular diferencia y cambio porcentual
        diferencia = tasa2 - tasa1
        cambio_porcentual = (diferencia / tasa1) * 100

        # Crear el gráfico
        fechas = [fecha1, fecha2]
        tasas = [tasa1, tasa2]

        plt.figure(figsize=(8, 5))
        plt.bar(fechas, tasas, color='skyblue', width=0.4)
        plt.title(f'Comparación de tasas: {base} -> {target}')
        plt.xlabel('Fecha')
        plt.ylabel('Tasa de Cambio')
        plt.grid(axis='y')
        plt.tight_layout()

        # Guardar el gráfico como imagen
        grafico_path = 'grafico_tasas.png'
        plt.savefig(grafico_path)
        plt.close()

        # Retornar datos numéricos y gráfico
        datos_texto = (
            f"📊 **Comparación de tasas entre {fecha1} y {fecha2}:**\n\n"
            f"🔹 Tasa en {fecha1}: 1 {base} = {tasa1:.6f} {target}\n"
            f"🔹 Tasa en {fecha2}: 1 {base} = {tasa2:.6f} {target}\n"
            f"🔹 Diferencia: {diferencia:.6f} {target}\n"
            f"🔹 Cambio porcentual: {cambio_porcentual:.2f}%\n\n"
        )
        return datos_texto, grafico_path
    return None, None

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("📋 Monedas soportadas")
    btn2 = types.KeyboardButton("💱 Tasas actuales")
    btn3 = types.KeyboardButton("📊 Comparar tasas entre fechas")
    markup.add(btn1, btn2, btn3)
    bienvenida = (
        "👋 ¡Hola y bienvenido al **Bot de Tasas de Cambio**! 🌍\n\n"
        "💵 Este bot te permitirá realizar las siguientes acciones:\n\n"
        "1️⃣ **Consultar monedas soportadas:** Descubre qué monedas puedes consultar.\n"
        "2️⃣ **Ver tasas actuales:** Conoce el valor actual de una moneda base en otras monedas.\n"
        "3️⃣ **Comparar tasas entre fechas:** Analiza cómo han cambiado las tasas de cambio entre dos fechas específicas.\n\n"
        "✨ ¡Selecciona una opción del menú para comenzar! 🚀"
    )
    bot.send_message(message.chat.id, bienvenida, reply_markup=markup)

# Respuesta a los botones
@bot.message_handler(func=lambda message: True)
def menu_response(message):
    if message.text == "📋 Monedas soportadas":
        monedas = obtener_monedas_soportadas()
        if monedas:
            mensaje = "🌍 **Monedas soportadas:**\n\n"
            for codigo, descripcion in monedas.items():
                mensaje += f"🔸 {codigo}: {descripcion}\n"
            bot.reply_to(message, mensaje)
        else:
            bot.reply_to(message, "❌ **No se pudieron obtener las monedas soportadas.**")

    elif message.text == "💱 Tasas actuales":
        bot.reply_to(message, "✍️ Escribe la **moneda base** (por ejemplo, USD):")
        bot.register_next_step_handler(message, obtener_tasas_base)

    elif message.text == "📊 Comparar tasas entre fechas":
        bot.reply_to(message, "✍️ Escribe la **moneda base** (por ejemplo, USD):")
        bot.register_next_step_handler(message, recibir_base_comparar)

# Funciones para comparación entre fechas
def recibir_base_comparar(message):
    user_data['base'] = message.text.upper()
    bot.reply_to(message, "✍️ Escribe la **moneda objetivo** (por ejemplo, EUR):")
    bot.register_next_step_handler(message, recibir_target_comparar)

def recibir_target_comparar(message):
    user_data['target'] = message.text.upper()
    bot.reply_to(message, "🗓️ Escribe la **primera fecha** en formato YYYY-MM-DD:")
    bot.register_next_step_handler(message, recibir_fecha1_comparar)

def recibir_fecha1_comparar(message):
    user_data['fecha1'] = message.text
    bot.reply_to(message, "🗓️ Escribe la **segunda fecha** en formato YYYY-MM-DD:")
    bot.register_next_step_handler(message, realizar_comparacion)

def realizar_comparacion(message):
    user_data['fecha2'] = message.text
    datos_texto, grafico = comparar_tasas_y_graficar(user_data['base'], user_data['target'], user_data['fecha1'], user_data['fecha2'])
    if datos_texto and grafico:
        bot.reply_to(message, datos_texto)
        with open(grafico, 'rb') as img:
            bot.send_photo(message.chat.id, img, caption="📊 **Aquí está el gráfico de comparación entre fechas.**")
    else:
        bot.reply_to(message, "❌ **No se pudieron obtener las tasas para las fechas seleccionadas.** Verifica que las fechas y monedas sean correctas.")

# Funciones para tasas actuales
def obtener_tasas_base(message):
    user_data['base'] = message.text.upper()
    bot.reply_to(message, "✍️ Escribe las **monedas objetivo** separadas por comas (por ejemplo, EUR,GBP):")
    bot.register_next_step_handler(message, mostrar_tasas_actuales)

def mostrar_tasas_actuales(message):
    monedas = message.text.upper().split(",")
    tasas = obtener_tasas_actuales(user_data['base'], monedas)
    if tasas:
        mensaje = f"💱 **Tasas actuales para {user_data['base']}:**\n\n"
        for moneda, tasa in tasas.items():
            mensaje += f"1 {user_data['base']} = {tasa:.6f} {moneda}\n"
        bot.reply_to(message, mensaje)
    else:
        bot.reply_to(message, "❌ **No se pudieron obtener las tasas actuales.**")

# Iniciar el bot
bot.polling()
