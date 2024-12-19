<h1 align="center"> Tarea 1: DCCampeonato 🏃‍♂️🏆 </h1>

* La siguiente tarea consiste en la simulacion de un campeonato que se compone de 4 rondas, el cual es jugado entre 16 jugadores (o entrenadores). Cada jugador tiene  diversos implementos para coronarse como campeón. Al inicio del juego,  debemos escoger  un entrenador de los 16, el cual posee distintas cualidades para ganar el campeonato.

* El código del juego consiste principalemnte en la utilizacion de clases abstractas, herencia, multiherencia, entre otros. Tambien creamos 5 archivos (especificados en *Librerías* :books:), los cuales permiten la interactividad entre el programa y el usuario.  

* Para un mejor entendimiento del código del juego, recomiendo comenzar desde el archivo ```dccampeonato.py```. Asimismo, en cada archivo hay detalles de la explicacion de cada clase, método o funcion implementado. 

## Consideraciones generales :octocat:
1. Al ejecutar el juego, se crearan "desde cero" todos los jugadores y sus programones con sus características respectivas en el archivo ```main.py```
2. Al iniciar el juego, el primer menu que se mostrará es el *menu de inicio*, en donde el jugador solo podra elegir uno de los 16 entrenadores totales. En el caso que quiera salir del juego, la ejecución del programa se terminará. 
3. En cada menú (expecto el de inicio) el jugador puede volver al menu anterior, en este caso tambien tiene la posibilidad de cambiar de entrenador si es que lo desea.   
4. Al finalizar la última ronda del campeonato, se comienza un nuevo campeonato. 
5. Existen dos casos al momento de simular una ronda del DCCampeonato: (1) si el jugador ganó su partida en la ronda actual (una ronda que no sea la final), su entrenador elegido reinicia su energia en 100 puntos, y vuelve al ```Menu Entrenador``` para seguir mejorando los atributos de nuestros programones; (2) si el jugador perdió su partida en la ronda actual del juego, el jugador podrá volver al menu de inicio o salir del juego.  



### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
#### Programación Orientada a Objetos (18pts) (22%%)
##### ✅ Diagrama
##### ✅ Definición de clases, atributos, métodos y properties		
##### ✅ Relaciones entre clases
#### Preparación programa: 11 pts (7%)			
##### ✅ Creación de partidas
#### Entidades: 28 pts (19%)
##### ✅ Programón
##### ✅ Entrenador		
##### ✅ Liga	
##### ✅ Objetos		
#### Interacción Usuario-Programa 57 pts (38%)
##### ✅ General	
##### ✅ Menú de Inicio
##### ✅ Menú Entrenador
##### ✅ Menu Entrenamiento
##### ✅ Simulación ronda campeonato
##### ✅ Ver estado del campeonato
##### ✅ Menú crear objeto
##### ✅ Menú utilizar objeto
##### ✅ Ver estado del entrenador
##### ✅ Robustez
#### Manejo de archivos: 12 pts (8%)
##### ✅ Archivos CSV
##### ✅ Parámetros
#### Bonus: 5 décimas
##### ❌ Mega Evolución
##### ❌ CSV dinámico

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```, el cual se ubica en el directorio ```T1```
1. ```main.py``` en ```T1```

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```random```, ```randint```, ```choice```, y ```choices```
2. ```abc```: ```ABC``` y ```abstractmethod```
3. ```entrenadores.csv```, ```programones.csv``` y ```objetos.csv```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```main.py```: Archivo principal que permite ejecutar e iniciar el programa. 
2. ```ligaprogramon.py```: Contiene la superclase ```LigaProgramon```
2. ```dccampeonato.py```: Contiene la subclase ```DCCampeonato``` heredada de la clase ```LigaProgramon```.
2. ```entrenadores.py```: Contiene la clase ```Entrenador```, y la clase abstracta ```Objetos``` la cual hereda las subclases ```Baya```, ```Pocion```, y ```Caramelo``` (también estan presentes en el archivo).
2. ```programon.py```: Contiene la clase abstracta ```Programon```y la subclases respectivas: ```Planta```,```Agua```,y ```Fuego``` 
2. ```parametros.py```: Contiene todos los parametros que afectan de manera especial en uno de los atributos de las entidades *Programon*, *Entrenador*, u *Objetos*. 

## Diagrama de clases DCCampeonato
Cada método de las clases creadas presentes en los archivos mencionados se pueden visualizar en el siguiente diagrama de clases. (La finalidad de cada método es explicada en notas escritas en su archivo respectivo). 

![Image text](https://github.com/IIC2233/pedrozavalat-iic2233-2022-2/blob/main/Tareas/T1/DiagramaDeClases.png)


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. La energia del entrenador no disminuirá cuando utiliza uno de sus objetos para aplicarlo en algun programon suyo. En este sentido, este podrá aplicar las veces que desee los beneficios de sus objetos en sus programones. 
2. Al momento de crear un objeto, se verificará que este no permanezca en la lista de objetos actuales que posee el entrenador. 
3. Si el jugador quiere volver jugar una partida luego de haber perdido una ronda, todas las caracácteristicas de los entrenadores y de los programones se restableceran. Es decir, sus objetos creados o los atributos mejorados de sus programones se pierden.   
4. En todos los casos el jugador podra salir del juego (excepto en los menús de ```Estado entrenador``` o ```Resumen Campeonato```). 
5. Si el jugador escoge un entrenador, está accion lo dirigirá al menu del entrenador respectivo, si el jugador se "arrepiente" de haber escogido aquel entrenador, puede volver al menu de inicio para escoger otro entrenador y asi simular el campeonato (con la opcion 'Volver'). 
6. En respecto al *punto 5*, por ejemplo: Sea el caso que el jugador ha realizado mejoras en los programones de un entrenador "A", y luego vuelve al menu de inicio a escoger un entrenador "B". Si el jugador no ha perdido con algun entrenador elegido, los cambios tanto de "A" como "B" aun quedan guardados. Ya si el jugador pierde o gana con alguno de los dos, los cambios se pierden dado que se comienza un nuevo campeonato.  
7. Los parametros en el archivo ```parametros.py``` fueron establecidos aleatoriamente. Dado que DCCampeonato solo tiene 4 rondas, el aumento de atributos de los programones son mas altos al mometno de entrenarlos, o aplicarles algun objeto, para asi que el entrenador tenga mas probabilidad de ganar. 
8. Si un programon presenta al maximo su vida, ataque o defensa. Los atributos como ataque, defensa, o vida no se veran alterados al momento de aplicarle los beneficios de un objeto, o entrenarlo. 

## Referencias de código externo :book:

Para realizar mi tarea saqué código principalmente:
1. \<../Tareas/T0>: Está implementado en el archivo ```ligaprogramon.py``` en las líneas 18 a 29. ```seleccionar_opción``` es un método que verifica que la respuesta entregada por el usuario pertenezca al rango del listado de opciones mostrado  en algun menu determinado. (Codigo extraído de mi Tarea 0)

