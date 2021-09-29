## Registro de cambios

## ePLIbidem 0.7
Esta versión añade el manejo automático para nuevos casos y pequeños ajustes a la interfaz, además de cambios internos del código.

### Cambios:
* Muestra atajos de teclado en la ayuda emergente.
* Muestra id de los ibíd. sin ajustar cuando quedan 8 o menos por editar.
* Ajuste automático en más casos tipo (con variantes):
    - `TEXTO_NOTA_BASE, págs. A y B.` e `Ibídem, págs. C y D.`
    - `TEXTO_NOTA_BASE, págs. X, Y.` e `Ibídem, pág. Z.`
* Ajuste y limpieza de código en tests de casos.
_____________________________

## ePLIbidem 0.6
Esta versión implementa el reemplazo automático de las páginas en casos sin ambigüedad al procesar las notas, además de mejoras internas del código.

### Cambios:
* Ajusta automáticamente los casos no ambiguos de notas base con números de páginas y las reemplaza por las páginas señaladas en el ibíd. sin agregar el separador. Por ejemplo, teniendo las notas `Nota p. 5` e `Ibíd. p. 6`, la salida del procesamiento automático será `Ibíd. Nota p.6`. En cambio en casos ambiguos, si la nota base fuera `Nota p. 5. Capítulo p. 6`, la salida sería `Nota p. 5. Capítulo p. 6 SEPARADOR: p. 6`.
* Detecta cuando se actualiza el plugin y restablece automáticamente a la configuración por defecto para evitar errores.
* Muestra la versión en la barra de título de la ventana.

### Corrección de errores:
* Corrige un pequeño error de tipeo en la regex que afectaba casos con tags del tipo `<i xml:lang="la">`.
* Guarda valores numéricos como int en lugar de strings.

_____________________________

## ePLIbidem 0.5
Esta versión mejora el análisis de las notas, limpia el formato de salida y corrige comportamientos para casos específicos.

### Cambios:
* Añadida la opción **Nada** al tag ibid.
* Ahora preserva textos adicionales dentro de `<h1>`, `<h2>`, etc. y `<p>`.
* RegEx optimizada para coincidir más casos.

### Corrección de errores:
* Ya no agrega espacios en blanco cuando dejamos vacíos los campos de separador e ibíd.
* Corregido </i> que agregaba el procesado de notas en casos con puntuación dentro del tag (<i>ibid.</i>).
* Corregidos pequeños detalles de formato al sobrescribir el xhtml.
