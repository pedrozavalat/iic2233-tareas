
<h1 align="center"> :zombie::seedling::sunflower: Tarea 2: DCCruz vs Zombies :zombie::seedling::sunflower: </h1>

### Flujo del juego :seedling:

La siguiente tarea **DCCruz vs Zombies** consiste en la simulacion del juego original *Plantas vs Zombies*. El siguiente juego fue realizado mediante los siguientes aspectos reflejados en el codigo. En primer lugar, el juego comenzara con la **Ventana de Inicio**, en donde se presenta una etiqueta para escribir nuestro nombre de usuario (el cual debe cumplir ciertas condiciones), y los botones: *Salir*, *Jugar*, y *Ranking*. Por un lado, el boton Salir termina la ejecucion de la ventana y la cierra, mientras que, el boton Ranking nos muestra una *Top 5* de los mejores puntajes. Por otro lado, esta el boton Jugar, el cual comienza el juego. Despues de iniciar el juego, se mostrará la **Ventana Principal** con el escenario a elegir (de forma obligatoria). Luego del escenario elegido, se abrira el juego, con la tienda de las plantas a escoger, y las opciones *Iniciar*, *Avanzar*, *Pausa*, y *Salir*. Ya finalmente, al terminar el juego (ganado, o perdido), se abrirá la **Ventana Post Juego**. Si el jugador ganó, podra optar por seguir jugando una nueva ronda, o, salir del juego. En el caso, el jugador perdiera, este solo podra volver a la **Ventana de Inicio**.
  
## Consideraciones generales :octocat:

Durante la tarea, el flujo entre ventanas pudo ser posible. Sin embargo, hay ciertos aspectos en la logica del juego los cuales no pude implementar, u otros que presentan alguna 'notificacion' en el terminal.

#### Detalles del flujo del juego 👨🏻‍💻

- **La primera vez** que se inicia la Ventana del *Ranking*, este presentará correctamente de forma ascendente los *Top 5 Jugadores* del juego, sin notificar nada en el terminar. Pero, por ejemplo, si se vuelve al inicio y se presiona nuevamente la ventana del ranking, se notificara el mensaje 
```
QWidget::setLayout: Attempting to set QLayout "" on VentanaRanking "", which already has a layout
``` 
 Esto no altera el ranking, pero se notifica siempre que se quiera acceder nuevamente al ranking, siempre y cuando, no hayamos cerrado el juego. 

- Cuando ya hayamos elegido un escenario, y luego el jugador quiere volver al inicio, para asi nuevamente empezar otra partida, **el boton del escenario elegido anteriormente queda aun seleccionado**. Por ejemplo: Al comenzar el juego por primera vez, ambos botones *no estan seleccionados*. Luego, si elijo un escenario (p.e, Salida nocturna), y después salgo del juego, volviendo a la ventana de inicio, al momento de querer empezar una nueva partida y elegir un escenario distinto, el boton del escenario Salida Nocturna queda seleccionado. **Esto no afecta al momento de iniciar el juego**, pero si es un detalle. 

- Durante el juego, logre posicionar las plantas dentro del tablero del escenario. Sin embargo, cuando una planta es comida por un zombie y desaparece, **no podremos agregar una nueva planta en la posicion de la planta que 'fue comida'**. Esto no afecta en las rondas siguientes, pero durante el juego de la ronda actual, nos afecta si es que queremos agregar una nueva planta en la posicion de una planta que fue eliminada. 

- Algunos *Sprites* del juego, como el lanza guisantes o el zombie rapido, durante su movimiento cambian un poco su tamaño. Fue un detalle que no logre arreglar :(

#### Aspectos del juego que no pude implementar 🥲
- Dentro de los movimientos de las plantas, un aspecto que no pude implementar fue el movimiento de la colision de los proyectiles de las plantas Lanza Guisantes (Clasicas y de Hielo). Estos logran desaparecer cuando colisionan con un zombie, pero no presentan aquel "efecto de explosion" al momento de chocar. 

- Asimismo, otro aspecto que no pude implementar fue el intervalo de tiempo de mordida sobre las plantas cuando un zombie las ataca. Aun asi, logre realizar la animacion de los zombies cuando se comen una planta, pero no en el tiempo debido. En este caso, el tiempo que se demoran en mi codigo es menor. 

## Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Ventanas: 39 pts (40%)
##### ✅ Ventana de Inicio
##### ✅ Ventana de Ranking	
##### ✅ Ventana principal
##### ✅ Ventana de juego	
##### ✅ Ventana post-ronda
#### Mecánicas de juego: 46 pts (47%)			
##### ✅ Plantas
##### ✅ Zombies
##### ✅ Escenarios		
##### ✅ Fin de ronda	
##### ✅ Fin de juego	
#### Interacción con el usuario: 22 pts (23%)
##### ✅ Clicks	
##### 🟠 Animaciones
#### Cheatcodes: 8 pts (8%)
##### ✅ Pausa
##### ✅ S + U + N
##### ✅ K + I + L
#### Archivos: 4 pts (4%)
##### ✅ Sprites
##### ✅ Parametros.py
##### ✅ K + I + L
#### Bonus: 9 décimas máximo
##### ❌ Crazy Cruz Dinámico
##### ❌ Pala
##### ❌ Drag and Drop Tienda
##### ❌ Música juego

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```
1. ```main.py``` en ```Directorio principal```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```
2. ```sys```
3. ```random```: ```randint```, ```choice```
4. ```math```: ```ceil```


### Librerías propias 🙌🏻

En primer lugar, en el directorio principal se presentan el modulo creado:
* ```main.py```: Instancia todas las clases de los archivos de las ventanas de la carpeta ```frontend``` y las clases de las logicas respectivas ubicadas en la carpeta ```backend```. También, permite ejecutar el programa y  realiza todas las conexiones entre el frontend y el backend. 

En segundo lugar, en la carpeta ```frontend```  los módulos que fueron creados fueron los siguientes: 

1. ```ventana_inicio.py```: Contiene la clase ```VentanaInicio```. Posee todos los aspectos visuales de la **Ventana de Inicio** (Iniciar juego, salir juego, ver ranking, e ingresar usuario). 

2. ```ventana_ranking.py``` : Contiene la clase ```VentanaRanking```.Ilustra el ranking de los top 5 jugadores de DCCruz vs Zombies. 

3. ```ventana_principal.py```: Contiene la clase ```VentanaPrincipal```. Contiene las opciones de los escenarios a elegir (***Jardin de la abuela*** o ***Salida Nocturna***).

4. ```ventana_juego.py```: Contiene la clase ```VentanaJuego```. Contiene todos los metodos que permiten comunicarse con su backend. 

5. ```ventana_post_ronda.py```: Contiene la clase ```VentanaPostRonda```. Contiene los metodos que permiten mostrar el tablero final al finalizar una ronda. 



Y por ultimo, en la carpeta ```backend``` los módulos que fueron creados fueron los siguientes: 

1. ```logica_inicio.py```: Contiene la clase ```LogicaInicio```. Verifica que el nombre ingresado cumpla las condiciones minimas solicitadas. 

2. ```logica_ranking.py``` : Contiene la clase ```LogicaRanking```. Actualiza el ranking de los *top 5*, ordenando ascendentemente los jugadores. 

3. ```logica_principal.py```: Contiene la clase ```LogicaPrincipal```. Verifica la seleccion del escenario. 

4. ```logica_juego.py```: Contiene la clase ```LogicaJuego```. Realiza todo el mecanismo del juego, como: el movimiento de las plantas, zombies, proyectiles; posicionar plantas; actualizacion de datos; entre otros. 

5. ```logica_botones.py```: Contiene la clase ```LogicaBotones```. Verifica la seleccion del boton *Pausa*, y los *Cheatcodes* K+I+L y S+U+N. 

6. ```elementos_del_juego.py```: Contiene las clases ```Soles```, ```ProyectilVerde```, y ```ProyectilAzul```.  

7. ```plantas.py```: Contiene las clases ```Girasol```, ```PlantasVerdes```, ```PlantasAzules```, y ```Patatas```.   

8. ```zombies.py```: Contiene las clases ```ZombieClasico```, y ```ZombieRapido```. 

9. ```funciones_utiles.py```: Contiene las funciones ```otorgar_ptje``` y ```otorgar_ptje_extra```. Retornan el puntaje concedido al eliminar un zombie, o eliminar todos los zombies, respectivamente. 

10. ```logica_post_ronda.py```: Contiene la clase ```LogicaPostRonda```. Verifica si el jugador perdio o ganó, para asi avanzar a una ronda, o salir del juego.  


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Si un jugador quiere comenzar una nueva partida con un mismo nombre de jugador utilizado anteriormente, entonces los datos del archivo ```puntaje.txt``` de la partida guardada con el nombre de usuario utilizado se borran. Por ejemplo, si ya jugué con el usuario *pedro123*, y obtuve *1200* puntos, entonces al comenzar una nueva partida con el mismo nombre de usuario, el puntaje respectivo será *0*.

2. Al utilizar los **cheatcodes** ```K+I+L``` y ```S+U+N``` para antes de iniciar una partida, los cambios no se veran reflejados. Estos se ilustrarán **solo cuando se inicie la partida** al presionar el boton **Iniciar**. 

3. Retomando el punto 2, cabe recalcar que los ***cheatcodes*** funcionaran **si y solo si se presionan las teclas consecutivamente**. Para poder guiarse en las teclas que uno presiona, durante la ejecucion se ve en el terminal del juego la linea: 
```
Secuencia de botones realizados: sun
``` 
para asi poder ver la secuencia de 3 caracteres que vamos presionando. 

4. Para el intervalo de tiempo en la aparicion de zombies durante las rondas del juego, el valor retornado por la funcion ```aparicion_zombies.py``` fue multiplicada por **10000** para dar una distancia adecuada entre los zombies durante su aparicion, dado que el valor retornado por la funcion era muy pequeño para poder ser utilizado como intervalo de tiempo en un QTimer. 

5. Tambien, en respecto a los zombies, la velocidad de movimiento fue adecuada para permitir un flujo correcto durante el juego. En el archivo ```zombies.py``` ubicado en la carpeta ```backend``` se encuentran los Timers ```timer_caminata```, ```timer_desplazamiento```, y ```timer_mordida```. (tanto para ZombieClasico como para ZombieRapido), los cuales presentan un intervalo de tiempo en respecto a la velocidad del zombie.
```python
...
self.timer_caminata = QTimer()
self.timer_caminata.setInterval(ceil(self.velocidad // 15)) 
self.timer_caminata.timeout.connect(self.caminata)

self.timer_desplazamiento = QTimer()
self.timer_desplazamiento.setInterval(ceil(150 - self.velocidad // 100))
self.timer_desplazamiento.timeout.connect(self.desplazamiento)

self.timer_mordida = QTimer()
self.timer_mordida.setInterval(ceil(self.velocidad))
self.timer_mordida.setSingleShot(True)
self.timer_mordida.timeout.connect(self.comiendo)
...
```
Las operaciones tanto para el ```timer_caminata```, como ```timer_desplazamiento```fueron con el objetivo de presentar una mejor fluidez y sentido del movimiento de los zombies durante el juego. ya que, el valor de la velocidad era muy grande para utilizarlo como intervalo de tiempo. Esta dinamica tambien se realiza en metodo del efecto de ralentizacion, en donde determinamos un nuevo tiempo de intervalo. 
```python 
self.timer_desplazamiento.setInterval(150 + ceil(self.velocidad // 100))
```
6. Asumí que el efecto de ralentizacion producido por los proyectiles generados por los lanza guisantes de hielo, provocan que el zombie permanezca a una velocidad menor a la original en todo el juego.

7. Finalmente, el puntaje extra otorgado cuando el jugador elimina todos los zombies es ilustrado en la ventana post-ronda. Es decir, este no se ve reflejado en el tablero de puntaje de la Ventana del juego, pero si en la Ventana Post Ronda.  


## Descuentos 
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/master/Tareas/Descuentos.md).
