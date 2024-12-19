![Image text](https://github.com/IIC2233/pedrozavalat-iic2233-2022-2/blob/main/Tareas/T3/dccardjitsu.png)
<h1 align="center">  💧❄️🔥 Tarea 3: DCCard-Jitsu 🔥❄️💧 </h1>

### Flujo del juego 🏁

La siguiente tarea DCCard-Jitsu consiste en la simulacion del juego original Card-Jitsu de Club Penguin. El siguiente juego fue realizado mediante los siguientes aspectos reflejados en el codigo. En primer lugar, se ejecutará el **servidor**, el cual permitirá las conexiones con los clientes, y luego para cada cliente conectado, se le abrirá la **Ventana de inicio** del juego DCCard-Jitsu. En esta podran escribir un nombre que quieran utilizar para el resto de la partida. Luego, deberan esperar en la **Ventana de Espera** hasta que otro jugador (cliente) se conecte al servidor. Si hay dos jugadores en la sala de espera, comenzará una cuenta regresiva de 10 segundos antes de comenzar el juego. Luego de haber terminado la cuenta regresiva, se abrira la **Ventana Juego**, en la cual presenta un tablero con las cartas de cada jugador y el tiempo de la ronda. Cada vez que un jugador gane, se le acumularan fichas correspondientes al elemento (agua, fuego, o nieve) y color (azul, rojo,o verde) de la carta utilizada. Finalmente, cuando uno de los dos jugadores haya acumulado tres fichas de distintos colores, todas del mismo elemento (o distinto elemento), este sera el ganador de la partida. Asimismo, se abrirá **Ventana Final** que notificara el ganador y perdedor de la partida. 

Tambien, existen otras ventanas durante el flujo del juego. Por ejemplo, por un lado, esta la **Ventana Error**, que se abre solamente cuando se pierde la conexion con el servidor. Esta se presentará por solo 3 segundos, y luego cerrara el programa para todos los clientes conectados. Por otro lado, esta implementado durante el juego la **Ventana Chat**, la cual permite intercambiar mensajes con el jugador oponente durante la partida del juego. Esta se visualiza solamente durante la partida. 

## Consideraciones generales 📣
Durante la tarea, gran parte de la comunicacion con el servidor en frente de multiples clientes pudo ser posible, pero hay excepciones que no permiten ciertos aspectos del flujo del juego.

#### Detalles del flujo del juego 👨🏻‍💻
- Antes que todo, cuando un Cliente ejecuta su programa con un servidor activo, se le notificará dentro de su terminal el siguiente codigo
```
QCssParser::parseColorValue: Specified color with alpha value but no alpha given: 'rgba 83, 175, 252'
``` 
Esto no influye en el flujo del juego pero es un detalle.
- Algo muy **importante** de mencionar es que, cuando iniciamos el servidor, para que se permita el inicio del juego, primero debemos ingresar un cliente a la sala de espera, y luego consecutivamente abrimos otra ventana para el jugador siguiente. Esto se debe a que cuando se abren dos ventanas de inicio al mismo tiempo (aun sin ingresar a los jugadores), en la ventana de espera no se cargaran los usuarios. En este sentido, el terminal del servidor lanza un ```KeyError``` dado que los usuarios se guardan con el mismo id. Fue un error que no logre solucionar. 


#### Aspectos del juego que no pude implementar 🥲
- Uno de los aspectos importantes que no pude implementar fue los archivos ```cripto.py``` para la comunicacion entre el servidor y el cliente. A pesar de que las funciones ```desencriptar```y ```encriptar```cumplen su objetivo, cuando las implementé en la comunicación, el cliente no recibia las respuestas del servidor. Por lo tanto, preferí no usarlas en el codigo :(. 

- Otro  error importante es la **sala de espera**. Esta solo funciona para la primera partida. Es decir, funciona perfectamente en el momento que se conectan dos usuarios, comenzando la cuenta regresiva. Sin embargo, esta presenta errores, cuando un usuario decide volver a la ventana de inicio. Dado que, en el momento en que el cliente decide salir de la sala de espera, y luego volver, el boton para ingresar a la ventana de espera se bloquea y no le permite ingresar. Asimismo, cuando termina una partida entre dos usuarios, y luego otros jugadores quieren ingresar al juego, la ventana de espera  no actualiza los nombres de los nuevos jugadores.

- Finalmente, un detalle que uno debe considerar es que durante la partida, **si ambos jugadores no eligen cartas**, el juego no actualiza la interfaz de las cartas elegidas. Es decir, la eleccion de una carta aleatoria solo funciona cuando un jugador no elige una carta, pero el otro jugador si. 
  
### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Networking: 26 pts (19%)
##### ✅ Protocolo	
##### ✅ Correcto uso de sockets		
##### ✅ Conexión	
##### ✅ Manejo de Clientes	
##### ✅ Desconexión Repentina
#### Arquitectura Cliente - Servidor: 31 pts (23%)			
##### ✅ Roles			
##### ✅ Consistencia		
##### ✅ Logs
#### Manejo de Bytes: 27 pts (20%)
##### ✅ Codificación			
##### ✅ Decodificación			
##### ❌ Encriptación		
##### ❌ Desencriptación	
##### 🟠 Integración
#### Interfaz Gráfica: 27 pts (20%)	
##### ✅ Ventana inicio		
##### ✅ Sala de Espera			
##### ✅ Ventana de juego							
##### ✅ Ventana final
#### Reglas de DCCard-Jitsu: 17 pts (13%)
##### ✅ Inicio del juego			
##### ✅ Ronda				
##### ✅ Termino del juego
#### Archivos: 8 pts (6%)
##### ✅ Parámetros (JSON)		
##### ✅ Cartas.py	
##### ❌ Cripto.py
#### Bonus: 8 décimas máximo
##### ✅ Cheatcodes	
##### ❌ Bienestar	
##### ✅ Chat

## Ejecución :computer:
Los modulos principales a ejecutar son llamados ```main.py```, los cuales son tanto para el cliente como el servidor.
1. ```main.py``` en ```/servidor```
2. ```main.py``` en ```/cliente```

Ambas carpetas ```/servidor``` y ```/cliente``` se deben encontrar en su ```Directorio Principal```. 

# Librerías :books:
## Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```
2. ```threading```
3. ```json```
4. ```socket```
5. ```pyparsing```
6. ```random```
7. ```os```
8. ```collections```


## Librerías propias - Servidor
Por un lado, en la carpeta **servidor**, se encuentran los siguientes modulos creados:

1. ```parametros.json```: Modulo que presenta todos los parametros o constantes utilizadas en el juego. Como por ejemplo, el Host y el Port utilizado para el programa. 

2. ```funciones_utiles.py```: Presenta la funcion ```cargar_data_json```, la cual retorna el valor de un parametro buscado desde el archivo ```parametros.json```. 

3. ```servidor.py```: Archivo que permite la conexion del servidor con cada cliente. Asimismo, involucra la codificacion y decodificacion de los mensajes enviados o recibidos con los clientes. Y tambien presenta modulos apartes (como ```self.enviar_mensaje```, ```self.actualizar_sala_espera```, entre otros) los cuales permiten comunicarse con todos los clientes del juego al mismo tiempo. 

4. ```logica.py```: Archivo que permite procesar los mensajes recibidos por parte del cliente. 

5. ```main.py```: Archivo que permite la ejecución del servidor. 
                    


## Librerías propias - Cliente
Por otro lado, en la carpeta **cliente** se encuentrar los siguientes modulos creados:

1. ```parametros.json```: Modulo que presenta todos los parametros o constantes utilizadas en el juego. Como por ejemplo, el host y el port utilizado para el programa; el tiempo de la cuenta regresiva utilizado en el juego; la cantidad de cartas que debe presentar cada cliente en su interface, entre otros. 

2. ```funciones_utiles.py```: Presenta la funcion ```cargar_data_json```, la cual retorna el valor de un parametro buscado desde el archivo ```parametros.json```. 

3. ```main.py```: Archivo que permite la ejecución del cliente.

Asimismo dentro de la misma carpeta cliente, se encuentran las carpetas:

- ```/cliente/frontend```: Presenta todas las interfaces gráficas utilizadas para la ejecucion del programa del cliente. 
- ```/cliente/backend```: Presenta toda la lógica con respecto a las interfaces graficas y la comunicacion con el servidor. 

En la carpeta ```backend``` se encuentran los siguientes archivos:

1. ```cliente.py```: Permite la conexion con el servidor. Permite enviar y recibir mensajes con el servidor. 

2. ```logica_interfaz.py```: Por un lado presenta todo la logica de procesamiento de los mensajes recibidos por parte del servidor. Mientras que ademas, por otro lado, contiene multiples metodos para la interaccion y envio de señales con el *frontend*. 

3. ```elementos_del_juego.py```: Presenta la clase ```Carta```, la cual contiene los atributos de cada carta (color, elemento y puntaje). 

Mientras que en la carpeta ```frontend```, se encuentras los siguientes modulos de cada interfaz gráfica utilizada en el juego, como:
1. ```ventana_inicio.py```: Contiene la clase ```VentanaInicio```, en donde permite la validacion del login del usuario.

2. ```ventana_espera.py```: Contiene la clase ```VentanaEspera```, en donde se ilustra los usarios que estan esperando una nueva partida. 

3. ```ventana_juego.py```: Contiene la clase ```VentanaJuego```. Contiene todos los elementos necesarios (como la baraja del usuario, el tiempo de la cuenta regresiva, entre otros) para la actualizacion de la interfaz del usuario al momento de jugador con otro cliente. 

4. ```ventana_final.py```: Contiene la clase ```VentanaFinal```. Permite notificar si el cliente fue ganador de la partida o perdedor. 

5. ```ventana_chat.py```: Contiene la clase ```VentanaChat```. Esta ventana permite la comunicacion del usuario con otro jugador en tiempo real durante la partida. Esta se abrirá solemente cuando se inicia un juego (es decir, cuando se abre la **Ventana Juego**).

6. ```ventana_error.py```: Contiene la clase ```VentanaError```. Esta se abre solamente en *casos de emergencia*, en donde el servidor deja de ejecutar el programa. En consecuencia, cada cliente es desconectado del servidor, en donde antes de cerrar su programa se les notifica por unos 3 segundos el mensaje *Ha ocurrido un error con el servidor, intenta mas tarde*. 

![Image text](https://github.com/IIC2233/pedrozavalat-iic2233-2022-2/blob/main/Tareas/T3/VentanaError.png)

ademas se presenta la carpeta ```assets```, en donde contiene los archivos de QtDesigner para cada interfáz gráfica. 


# Supuestos y consideraciones adicionales :thinking:
Para esta tarea realice los siguientes supuestos:
- La cuenta regresiva de la ventana de espera es de 10 segundos, dado que pense que era lo mas cómodo para los jugadores para la espera del comienzo del juego. 

- Durante la partida del juego, si un jugador selecciona una carta del tablero, esta se mostrara tanto para él como su oponente, solo que al otro usuario (el oponente) se mostrara la parte trasera de la carta. 

- Cuando se gana una ronda, se presentara un tiempo de espera de no mas de 3 segundos para que los jugadores puedan visualizar quien ganó, perdio, o si hubo un empate.

- En el caso que un jugador sale de la partida, si el otro jugador que aun esta en juego apreta un click, recien se le notificará que es ganador de la partida.

- Una consideracion importante es que el servidor no presenta una comunicacion 'rapida' con el cliente al momento en donde este cierra su programa. Ya que, cuando el cliente sale del programa, se demora un tiempo de 15 a 30 segundos en donde el servidor se le notifica dentro de su log lo siguiente:
```
...
|------------------------------|------------------------------|------------------------------------------------------------|
|              -               |       Usuario Offline        |               Se ha desconectado un usuario                |
|------------------------------|------------------------------|------------------------------------------------------------|
...
```

- Un aporte para el cheatcode **V + E + O**, el cual nos permite visualizar las cartas de nuestro rival, es que en nuestro terminal deje como ayuda la secuencia de botones que uno realiza. Dado que este cheatcode solo **funciona de manera secuencial**. Al mostrar las cartas del oponentes, estas se visualizan por solo 3 segundos. 
```
Secuencia de botones realizados: veo
Secuencia de botones realizados: ove
```
- La ventana chat permite la visualizacion de solo los usuarios presentes en el juego, en donde muestra los ultimos 10 mensajes enviados. En este sentido, los mensajes que no aparecen en la interfaz se van eliminando. 
![Alt Text](https://media.giphy.com/media/2f6gZBtoleXuvQiDSO/giphy.gif)

## Referencias de código externo :book:

La actividad formativa 3 (AF3) fue clave para la base de mi codigo, principalmente para la estructura de los archivos ```cliente.py``` y ```servidor.py```. En este sentido para los metodos de las clases ```Servidor``` y ```Cliente```, como:

| Servidor | Cliente |
| :---: | :---: |
| ```iniciar_cliente``` | ```iniciar_servidor``` |
| ```comenzar_a_aceptar_conexiones``` |```comenzar_escuchar_servidor``` |
| ```escuchar_cliente``` |```escuchar_servidor``` |
| ```enviar_mensaje``` |```enviar_mensaje``` |
| ```recibir_mensaje``` |```recibir_mensaje``` |
| ```codificar_mensaje``` |```codificar_mensaje``` |
| ```decodificar_mensaje``` |```decodificar_mensaje``` |

la estructura del codigo fue guiada en base a la presentacion *Semana 9 - Networking (cierre)*, en donde menciona la solucion de los archivos ```servidor.py```y ```cliente.py``` de la AF3 2022 2.  

## Descuentos 
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/master/Tareas/Descuentos.md).

