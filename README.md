ALUMNOS: CAFFARELLI, HIERREZUELO, BROTTO
MATERIA: PROGRAMACIÓN II
FECHA DE ENTREGA: 21/11/24
NOMBRE DEL PROYECTO: “TuConversor”

Resumen “Tu Conversor”
El proyecto TuConversor nació como una idea para simplificar el acceso a la información sobre tasas de cambio de monedas, algo que puede ser complejo para muchos usuarios. Con este chatbot de Telegram, cualquier persona puede consultar valores actualizados y realizar comparaciones de manera interactiva y amigable.
El bot utiliza la API ForexRateAPI para obtener datos en tiempo real y datos históricos, permitiendo responder preguntas como:
¿Cuánto vale mi moneda en otras divisas?
¿Cómo ha cambiado la tasa de cambio en los últimos años?
Además, incluye gráficos para visualizar comparaciones entre fechas, lo que hace que la información sea más fácil de entender. Nuestro enfoque siempre fue crear una herramienta práctica y accesible que pudiera ser útil tanto para usuarios sin experiencia como para aquellos que buscan datos más avanzados.

Objetivos
El principal objetivo era desarrollar un chatbot en Telegram que pudiera:
Mostrar tasas de cambio actualizadas y confiables.
Comparar tasas históricas entre fechas específicas.
Generar gráficos claros que ayuden a visualizar los datos.
Ser fácil de usar, con mensajes y explicaciones claras para cualquier usuario.
Queríamos que el bot no solo funcionara bien, sino que también fuera atractivo y útil, permitiendo a los usuarios tomar decisiones mejor informadas.

Por qué elegimos estas herramientas
Telegram Bot API:
Telegram es una plataforma ampliamente utilizada, y su API nos permitió crear un bot con opciones personalizables y fáciles de integrar.
ForexRateAPI:
Aunque inicialmente usamos otra API (ExchangeRate-API), descubrimos que ForexRateAPI era más completa y ofrecía datos históricos, una función esencial para el proyecto.
Python:
Python fue el lenguaje ideal por su facilidad de uso y la disponibilidad de bibliotecas como:
requests: para conectarnos con la API.
matplotlib: para crear gráficos visuales.
telebot: para construir la interfaz con Telegram.
Estas herramientas hicieron posible un desarrollo eficiente y un resultado de calidad.

Cómo funciona el bot
El bot ofrece tres funciones principales:
Consulta de monedas soportadas:
Permite conocer todas las monedas disponibles en la API junto con sus descripciones. Esto es útil para saber qué monedas se pueden consultar o comparar.
Tasas actuales:
Muestra cuánto vale una moneda base (como USD) en comparación con otras monedas seleccionadas. Los datos se obtienen en tiempo real, ofreciendo una visión clara de la situación actual del mercado.
Comparación de tasas entre fechas:
Permite comparar el valor de una moneda entre dos fechas específicas. Además, el bot genera un gráfico que muestra estas tasas de cambio, facilitando la interpretación de los datos.
Los usuarios pueden interactuar con estas funciones a través de botones en el menú principal, lo que hace que la experiencia sea sencilla y fluida.

Dificultades encontradas
No todo fue sencillo durante el desarrollo. Uno de los principales desafíos fue la limitación de la API inicial. Aunque ExchangeRate-API cumplía con algunos requisitos, carecía de datos históricos, algo solicitado por el profesor. Esto nos llevó a cambiar completamente a ForexRateAPI, lo que implicó ajustes en el código y nuevas pruebas.
También tuvimos que resolver problemas técnicos al integrar gráficos generados por matplotlib en los mensajes de Telegram. Sin embargo, con un enfoque detallado y pruebas constantes, logramos superar estos obstáculos.

Resultados obtenidos
El bot superó las expectativas iniciales. Algunas de las características más destacadas incluyen:
Funcionalidades completas: El bot ofrece todas las opciones planificadas, desde consultas simples hasta gráficos comparativos.
Interfaz amigable: Los mensajes son claros, con explicaciones y emojis que hacen que la interacción sea más agradable.
Gráficos visuales: Una de las mejoras más importantes fue la inclusión de gráficos que permiten visualizar las comparaciones de tasas de manera sencilla.
Manejo de errores eficiente: Si ocurre un problema (como una moneda o fecha inválida), el bot informa al usuario sin interrumpir su experiencia.

Perspectivas futuras
Aunque el proyecto está completo, siempre hay espacio para mejorar. Algunas ideas para el futuro incluyen:
Notificaciones automáticas: Informar a los usuarios sobre cambios significativos en las tasas de cambio.
Soporte multilenguaje: Hacer que el bot sea accesible para personas que hablen otros idiomas.
Gráficos más avanzados: Permitir comparaciones entre múltiples monedas en un solo gráfico.
Datos predeterminados: Facilitar el uso ofreciendo sugerencias automáticas si el usuario no ingresa información.

Conclusión
TuConversor es el resultado de semanas de trabajo, investigación y pruebas. Logramos crear un bot funcional que cumple con los objetivos propuestos y ofrece una experiencia positiva a los usuarios. Aunque enfrentamos desafíos, como el cambio de API, estos nos llevaron a un resultado final más completo y robusto.
Este proyecto no solo nos permitió aprender y aplicar conocimientos técnicos, sino también desarrollar una solución útil y práctica para cualquier persona interesada en tasas de cambio. TuConversor demuestra cómo la tecnología puede simplificar tareas complejas, haciendo que la información sea accesible para todos.
