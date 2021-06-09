# Registro de cambios

## ePLIbidem 0.6
Esta versión implementa el reemplazo automático de las páginas en casos sin ambigüedad al procesar las notas y contiene mejoras internas del código.

### Cambios:
* Ajusta automáticamente los casos no ambigüos de notas base con números de páginas y las reemplaza por las páginas señaladas en el ibíd. Por ejemplo teniendo las notas `Nota p. 5` e `Ibíd. p. 6`, la salida del procesamiento automático será `Ibíd. Nota p.6`.
* Detecta cuando se actualiza el plugin y restablece automáticamente a la configuración por defecto para evitar errores.
* Muestra la versión en la barra de título de la ventana.

### Corrección de errores:
* Corrige un pequeño error de tipeo en la regex que afectaba casos con tags del tipo `<i xml:lang="la">`.

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
