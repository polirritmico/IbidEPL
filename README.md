# **ePLIbidem** :book:
![ePLIbidem](docs/01.png?raw=true "ePLIbidem")

## **Descripción:**
Una pequeña herramienta para manejar las notas ibíd.

* **Requisitos:** _Sigil >0.9.8_

* **Instalación:** Igual a cualquier plugin de Sigil, menú Preferencias → Complementos → Añadir complemento. Allí se selecciona el zip con el plugin y pulsan Abrir. Opcionalmente pueden agregarlo a la barra de accesos rápidos.

* **Ejecución:** Primero abrir el xhtml con las notas o seleccionarlo en el Explorador del libro, a continuación abrir el plugin. Para que funcione, el archivo de notas debe seguir el estándar EPL. Se muestran recuadros de ayuda dejando el ratón sobre los elementos de la interfaz sin pulsar clic.

* **Link de descarga:** [versión 0.4](192.168.0.1)

* **Atajos de teclado:** :keyboard::computer_mouse:
    * **Ctrl + AvPág**: Abre nota ibid siguiente.
    * **Ctrl + RePág**: Abre nota ibid anterior.
    * **Ctrl + Retroceso** (Backspace): Procesar Ibid.
    * **Ctrl + Enter**: Reemplazar nota ibid.
    * **Ctrl + +**: Agrandar el tamaño del texto.
    * **Ctrl + -**: Reduce el tamaño del texto.

## **Funcionamiento:**
Por defecto el plugin agrega la etiqueta **\<i xml:lang="la">Ibíd\</i>** y el Separador **TEXTO_ADICIONAL:** (Ambas se pueden ajustar en la ventana de Opciones). El separador pretende ser solo una ayuda visual para diferenciar la nota original del ibíd. (e incluso para hacer búsquedas desde Sigil).

La idea es procesar la nota y luego hacer el ajuste manual en el mismo recuadro del ibid, que nos deja modificar el texto como queramos. El borde cambiará de color recordándonos que lo hemos editado pero que todavía no hemos guardado esas modificaciones. Cuando presionemos el botón Reemplazar estaremos realmente modificando la nota y luego cuando le demos a Aceptar se escribirán todos las modificaciones en el xhtml.

Si son muchas notas se puede utilizar el botón _Procesar y modificar todo_.
Se sugiere utilizar los atajos de teclado disponibles para las tareas más recurrentes.

## **Ejemplo de uso:**
1. Procesar la primera nota ibíd y ajustar manualmente su texto.
1. Luego presionar **Ctrl + Enter** para modificar la nota.
1. Pulsar **Ctrl + AvPág** para ir a la siguiente nota íbid.
1. Pulsar **Ctrl + Retroceso** para procesar la nota y ajustamos manualmente.
1. Repetimos 2 y 3 hasta terminar con todas las notas ibíd.
1. Pulsamos **Aceptar** para confirmar los cambios y sobrescribir el archivo de notas.

## **Controles:**
![Navigation](docs/02.png?raw=true "ePLIbidem")
1. Explorador de notas: Nos muestra la estructura de notas y sus ibid. Haciendo clic sobre cualquier ibíd. o nota nos lleva a ella.
1. Agranda o disminuye el tamaño del texto.
1. Avanza o retrocede a la siguiente nota, saltándose las notas ibid.
1. Avanza o retrocede a la siguiente nota ibid, saltándose las notas base.
1. Muestra la nota ibíd. y permite editar el texto.
1. Convierte la nota base a nota ibíd.
1. Convierte la nota ibíd a nota base.
1. Muestra la cantidad de notas ibid sin ajustar (en caso de haber procesado automáticamente todas las notas), y nos muestra las distintas notificaciones del plugin.
![Edit](docs/03.png?raw=true "ePLIbidem")
1. Aplica al texto los tag html (sólo para visualización). En este modo no se puede editar el texto. Cualquier cambio realizado en el texto sin modificar se descarta.
1. Restaura todos los cambios a la nota original (la leída del archivo).
1. Divide el recuadro del ibid actual y muestra la nota original arriba y la edición abajo. Útil para hacer una revisión de la edición.
1. Abre la ventana de configuración. Allí podemos:
   - Ajustar la REGEX (avanzado).
   - Cambiar el tag de la nota ibíd. (\<i xml:lang="la">Ibid\</i>).
   - Cambiar el texto del separador (Por defecto «TEXTO_ADICIONAL:»).
1. Ajusta automáticamente la nota ibíd. actual en base a la configuración.
1. Ajusta automáticamente en base a la configuración actual todas las notas ibíd. y guarda esos cambios.
1. Reemplaza la nota. Si la nota ibíd. tiene cambios con respecto a la nota ibíd. original, resaltará el cuadro del texto recordándonos que la nota tiene cambios que se perderán si es que no pulsamos este botón.
Además, mientras no se pulse el botón «Aceptar» (16), la modificación no se verá reflejada en el epub.
1. Escribe todos las modificaciones en el epub.
1. Descarta todos los cambios y deja el epub sin modificar.

---------------------------------------------

Bueno, espero sea de utilidad y ayude al proceso de maquetación del epub.

Saludos. :thumbsup:

