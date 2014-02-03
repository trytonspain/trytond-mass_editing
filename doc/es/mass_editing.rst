==============
Edición Masiva
==============

A |menu_mass_editing| dispondremos de la configuración para la edición de varios registros.
Dispondremos en los modelos un nuevo asistente que nos permitirá hacer modificaciones para varios
registros a la vez.

La edición masiva nos permite añadir, editar o eliminar valores en los campos de los registros
seleccionados.

Esta funcionalidad es muy común por ejemplo en los casos de los productos. Poder seleccionar
varios productos a la vez y hacer una edición en todos ellos con el mismo valor.

Configuración
-------------

Una Edición Masiva consiste en:

* Modelo con el que lo relacionamos
* Campos que dispondremos en el asistente para editar

Para disponer el asistente en el modelo para editar debemos accionar el botón "Crear asistente".
Esto nos creará un nuevo asistente disponible en el modelo.

El orden de los campos del asistente de edición será según a medida que el administrador vaya añadiendo
campos en la configuración de la "Edición masiva".

Uso
---

Accionaremos el asistente o acción que disponemos en el modelo. En este asistente nos listaran todos
los campos que se permiten hacer una edición.

Un campo para editar podremos escoger las opciones:

* Establecer. Añade o modifica el campo
* Eliminar. Elimina el contenido del campo

Para los campos relacionados dispondremos de más opciones:

* Eliminar. Elimina la opción seleccionada
* Eliminar todos. Nos elimina todos los valores del campo.

Campos requeridos
-----------------

En el caso que seleccionamos la opción de "Establecer" o "Eliminar" y no hemos introducido un valor
a modificar, nos alertará con un mensaje el campo requerido. Deberemos deseleccionar la opción si
no deseamos realizar ninguna tarea o rellenar un valor para ese campo.
