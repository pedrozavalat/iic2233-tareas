<h1 align="center"> Tarea 0: Start Advanced :rocket: </h1>

El siguiente proyecto consiste en la creación y ejecución del juego *Start Advanced*, el cual tiene como objetivo despejar todas las casillas de un tablero, con un tamaño personalizado por el jugador, para así encontrar las "bestias" del juego escondidas en él. En este sentido, cada casilla del tablero posee una bestia (representada como "N"), o un numero el cual representa la cantidad de bestias circundantes.  

Por un lado, el codigo del juego esta implementado por distintos tipos de librerías (incorporadas externamente, o creadas por mi), las cuales se relacionan entre si en el archivo principal del juego (archivo.py). El archivo.py esta construido en gran parte por estructuras de datos secuenciales y no secuenciales. En cambio, las librerías implementadas por mi (mencionadas en *Librerías* :books:) contienen funciones que permiten el flujo del juego. 

Tambien, por otro lado, gran parte de la descripción del codigo esta escrito brevemente en notas que fui dejando durante el desarrollo de la tarea. Por ello, para entender mejor el codigo del juego recomiendo empezar por el archivo.py. Este posee distintas funciones extraídas de otros archivos, en donde se describen en  mayor detalle las 'funcionalidades' que realizan cada una. 


## Consideraciones generales :octocat:

1. Al momento de cargar una partida, se mostrará solamente la ultima partida guardada por el usuario. Ya que, el usuario puede *guardar solo una partida*.
2. La carpeta que contiene al codigo considera una carpeta *'partidas'*, la cual contiene las partidas guardadas de otros usuarios que han jugado previamente. Sin embargo, si queremos eliminar aquellas partidas, recomiendo borrar la carpeta de las partidas anteriores y crear una nueva carpeta *'partidas'*, para asi tener las partidas creadas de nuestros usuarios.  
3. El juego *no* presenta la condicion de descubrimiento automático de casillas que no poseen bestias adyacentes (Bonus).
4. El *ranking de puntajes* considera *a lo más* las utimas 10 mejores partidas
5. El codigo archivo.py se visualiza bastante dos tableros principales: ```tablero```y ```tablero_bestias``` (son listas de listas). El primer tablero posee todos los *sectores descubiertos* por el jugador, con sus valores respectivos. Mientras que, el segundo tablero posee *todos los valores* de cada sector del tablero (es decir, considera tanto las casillas descubiertas como las que no están).
6. Para que el juego funcione correctamente, cada vez que queramos iniciar el juego, se debe crear un nuevo *terminal* en el archivo.py y luego ejecutar el código.
7. *Recomiendo descargar todos los archivos subidos y guardarlo en una carpeta llamada ```T0```*

### Cosas implementadas y no implementadas :white_check_mark: :x:

- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Programación Orientada a Objetos (18pts) (22%)
##### ✅  Menú de Inicio (Estructurado principalmente con "Built-in")
##### ✅ Funcionalidades		
##### ✅ Puntajes
#### Flujo del Juego (30pts) (36%) 
##### ✅ Menú de Juego
##### ✅ Tablero		
##### ✅ Bestias	
##### ✅ Guardado de partida		
#### Término del Juego 14pts (17%)
##### ✅ Fin del juego	
##### ✅ Puntajes	
#### Genera: 15 pts (15%)
##### ✅ Menús
##### ✅ Parámetros
##### ✅ PEP-8
#### Bonus: 3 décimas
##### ❌

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```archivo.py```, el cual se debe ejecutar en el directorio principal descargado ```T0```. Además,  en el caso de crear una nueva carpeta ```partidas```, esta se debe crear el siguiente directorio adicional:
1. ```partidas``` en ```T0```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas y sus funciones respectivas que utilicé fue la siguiente:

1. ```os``` : ```path``` y ```remove```
2. ```random``` :  ```randint``` y ```choice```
3. ```math``` : ```ceill```
4. ```string``` : ```ascii_lowercase```
5. ```tablero.py``` y ```parametros.py``` (Librerías entregadas por el enunciado)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```casillas.py```: Hecha principalmente para actualizar los datos de los tableros del juego.
	- Contiene las funciones:```ubicar_bestias```,```valores_casillas```, y ```flujo_juego```
2. ```verificaciones.py```: Hecha para verificar respuestas del usuario. 
	- Contiene las funciones: ```opcion_usuario```,  ```coordenadas```, y  ```medidas```  
3. ```partida.py```: Hecha para crear, guardar, y obtener el puntaje de una partida:
	- Contiene las funciones: ````nueva_partida````, ```guardar_partida```, ```cargar_partida```, ```calcular_puntaje``` y ```partida_ganada```. 

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Si un jugador quiere *cargar una partida*, pero esta no existe, entonces el jugador vuelve automaticamente al menu de inicio
2. Si un jugador guardó una partida previamente, y luego quiere cargar la misma partida. En el caso que gane (o pierda), los datos de la partida se borrara de la carpeta 'partidas'. 
3. Si un jugador no guarda una partida y luego sale del juego, esta partida se pierde. 
4. El formato de la partida guardada de un jugador consiste en un conjunto de coordenadas, tanto del tablero con los sectores descubiertos y el tablero con todas la coordenadas (considerando las posiciones de las N bestias). Es decir: 

```python 
...
(posicion x, posicion y) : valor \n 
...
#
...
(posicion x, posicion y) : valor \n
```
* Los datos de los dos tableros se dividen por un ```#```. En este caso, los datos que estan por sobre el # son del tablero con todas las posiciones *descubiertas* por el jugador, mientras que los datos que estan debajo del # son del tablero que presenta todos los valores para coordenada. 
5. Si existen dos partidas de usuarios distintos con el mismo puntaje, el ranking del juego se considerará en un lugar mas alto la partida 
que lleva mas tiempo guardada. 
6. En el ranking de puntajes se pueden mostrar todas las partidas jugadas de un usuario. Ademas, cada linea del tablero del ranking se muestra como: ```"Lugar" - "Nombre del usuario" - "Puntaje obtenido"```. El nombre del usuario y su puntaje respectivo se puede visualizar en el archivo ```puntajes.txt``` como: ``` nombre_usuario, puntaje_obtenido```
7. El nombre de usuario debe tener como máximo 15 carácteres (para así no alterar la tabla del ranking de puntajes)
8. Cuando el jugador quiere descubrir una nuevo sector del tablero, *la coordenada de la celda determinada* debe ser distinta a otras introducidas anteriormente. 
-------

## Metodos y funciones importantes
```python
class Main:

    def menu_inicio(self):
        ...
    ...
    
    def menu_juego(self, tablero_bestias, tablero):
        ...
```
La clase ```Main``` contiene dos metodos principales que permiten la interaccion entre el juego y el usuario. 
1. ```menu_inicio```: Muestra las opciones que quiere realizar el usuario antes de jugar (Empezar una nueva partida, Cargar una partida, Visualizar el ranking de puntajes, o Salir del juego)
2. ```menu_juego```: Muestra las opciones que quiere realizar el usuario durante el juego (Descubrir un nuevo sector, Guardar la partida, o Salir de la partida actual)

*Las descripciones de cada funcion utilizada en los metodos de la clase ```Main```estan explicadas detalladamente en el codigo de sus archivos respectivos (nombradas en la seccion de "Librerías Propias")*

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \https://replit.com/talk/learn/How-to-program-MineSweeper-in-Python-fully-explained-in-depth-tutorial/9397#part-6:-generating-the-solution-grid: El siguiente link explica un tutorial de crear en *Python* el juego *MineSweeper* (BuscaMinas en español). Durante la tarea me ayude en una parte del codigo de este tutorial (Parte 6 del tutorial).Este codigo, me sirvio principalmente para la estructura de las funciones ```ubicar_bestias```y ```valores_casillas```), ubicadas en el archivo ```casillas.py``` entre las líneas *24 a 77*. La función ```ubicar_bestias```  permite ubicar aleatoriamente la cantidad de N bestias sobre el tablero, mientras que ```valores_casillas```asigna valores a cada casillas segun las bestias que se encuentran adyacentes a una celda específica. Cabe recalcar que, ambas funciones no fueron copiadas textualemente de la pagina señalada, pero si fueron fuente de inspiracion y estructuración para la creacion del tablero del jugador al momento de crear una nueva partida. 


## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md).
