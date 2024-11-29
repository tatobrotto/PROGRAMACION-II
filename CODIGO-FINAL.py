import telebot
import requests
import matplotlib.pyplot as plt
from telebot import types
from datetime import datetime, timedelta

# Configuración del bot y la API
TOKEN = "7731934367:AAF66mTsggvvT6PEml0q4a95_PmNkzWyfLs"
API_KEY = "137c04948e734915b5e7db2cc9da2d77"
BASE_URL = "https://api.forexrateapi.com/v1"
bot = telebot.TeleBot(TOKEN)

# Configuración para la segunda API
SECOND_API_KEY = "c9188d620f890d6e2a6b47d0"
SECOND_BASE_URL = f"https://v6.exchangerate-api.com/v6/{SECOND_API_KEY}"

# Función para obtener la tasa de cambio usando la segunda API
def obtener_tasa_exchangerate(base, target):
    url = f"{SECOND_BASE_URL}/pair/{base}/{target}"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        if datos.get("result") == "success":
            return datos["conversion_rate"]
    return None

# Comando adicional para consultar con la segunda API
@bot.message_handler(func=lambda message: message.text == "🌐 Consultar con otra API")
def consulta_segunda_api(message):
    bot.reply_to(message, "✍️ Escribe la **moneda base** (por ejemplo, USD):")
    bot.register_next_step_handler(message, obtener_base_segunda_api)

def obtener_base_segunda_api(message):
    user_data['base'] = message.text.upper()
    bot.reply_to(message, "✍️ Escribe la **moneda objetivo** (por ejemplo, EUR):")
    bot.register_next_step_handler(message, obtener_target_segunda_api)

def obtener_target_segunda_api(message):
    user_data['target'] = message.text.upper()
    tasa = obtener_tasa_exchangerate(user_data['base'], user_data['target'])
    if tasa:
        bot.reply_to(
            message, 
            f"🌐 Tasa de cambio obtenida con ExchangeRate-API:\n\n"
            f"1 {user_data['base']} = {tasa:.6f} {user_data['target']}\n"
        )
    else:
        bot.reply_to(
            message, 
            "❌ **No se pudo obtener la tasa de cambio con la segunda API.**"
        )

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

# Función para analizar la evolución semanal de una moneda
def analizar_evolucion_semana(base, target, fecha_inicio):
    tasas = []
    fechas = []
    fecha_actual = datetime.strptime(fecha_inicio, "%Y-%m-%d")

    for i in range(7):
        fecha_str = fecha_actual.strftime("%Y-%m-%d")
        tasa = obtener_tasa_historica(base, target, fecha_str)
        if tasa is not None:
            tasas.append(tasa)
            fechas.append(fecha_str)
        fecha_actual += timedelta(days=1)

    if tasas:
        # Crear el mensaje de análisis
        mensaje = f"📊 **Evolución de la tasa semanal ({base} -> {target}):**\n\n"
        for i in range(len(tasas)):
            mensaje += f"🔹 {fechas[i]}: 1 {base} = {tasas[i]:.6f} {target}\n"

        cambio_total = tasas[-1] - tasas[0]
        cambio_porcentual = (cambio_total / tasas[0]) * 100
        mensaje += f"\n🔹 **Cambio total:** {cambio_total:.6f} {target}\n"
        mensaje += f"🔹 **Cambio porcentual:** {cambio_porcentual:.2f}%\n"

        # Generar el gráfico
        plt.figure(figsize=(8, 5))
        plt.plot(fechas, tasas, marker="o", color="b", label=f"Tasa {base} -> {target}")
        plt.title(f"Evolución semanal: {base} -> {target}")
        plt.xlabel("Fecha")
        plt.ylabel("Tasa de cambio")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Guardar el gráfico como archivo en memoria
        grafico_path = "evolucion_semanal.png"
        plt.savefig(grafico_path)
        plt.close()

        return mensaje, grafico_path
    else:
        return "❌ **No se encontraron datos para la semana seleccionada.**", None

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton("📋 Monedas soportadas")
    btn2 = types.KeyboardButton("💱 Tasas actuales")
    btn3 = types.KeyboardButton("📊 Comparar tasas entre fechas")
    btn4 = types.KeyboardButton("📈 Analizar evolución semanal")
    btn5 = types.KeyboardButton("🌐 Consultar con otra API")  # Nueva opción
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bienvenida = (
        "👋 ¡Hola y bienvenido al **Bot de Tasas de Cambio**! 🌍\n\n"
        "💵 Este bot te permitirá realizar las siguientes acciones:\n\n"
        "1️⃣ **Consultar monedas soportadas:** Descubre qué monedas puedes consultar.\n"
        "2️⃣ **Ver tasas actuales:** Conoce el valor actual de una moneda base en otras monedas.\n"
        "3️⃣ **Comparar tasas entre fechas:** Analiza cómo han cambiado las tasas de cambio entre dos fechas específicas.\n"
        "4️⃣ **Analizar evolución semanal:** Visualiza cómo varió una moneda durante una semana específica.\n"
        "5️⃣ **Consultar con otra API:** Consulta una tasa de cambio básica usando ExchangeRate-API.\n\n"
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

    elif message.text == "📈 Analizar evolución semanal":
        bot.reply_to(message, "✍️ Escribe la **moneda base** (por ejemplo, USD):")
        bot.register_next_step_handler(message, recibir_base_evolucion)

# Funciones para evolución semanal
def recibir_base_evolucion(message):
    user_data['base'] = message.text.upper()
    bot.reply_to(message, "✍️ Escribe la **moneda objetivo** (por ejemplo, EUR):")
    bot.register_next_step_handler(message, recibir_target_evolucion)

def recibir_target_evolucion(message):
    user_data['target'] = message.text.upper()
    bot.reply_to(message, "🗓️ Escribe la **fecha de inicio** de la semana en formato YYYY-MM-DD:")
    bot.register_next_step_handler(message, realizar_analisis_semanal)

def realizar_analisis_semanal(message):
    fecha_inicio = message.text
    mensaje, grafico = analizar_evolucion_semana(user_data['base'], user_data['target'], fecha_inicio)
    if mensaje and grafico:
        bot.reply_to(message, mensaje)
        with open(grafico, "rb") as img:
            bot.send_photo(message.chat.id, img, caption="📊 **Aquí está el gráfico de la evolución semanal.**")
    else:
        bot.reply_to(message, "❌ **No se pudieron obtener las tasas para la semana seleccionada.**")

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
