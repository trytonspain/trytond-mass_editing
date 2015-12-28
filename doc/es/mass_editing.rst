==============
Edición Masiva
==============

En el menu |menu_mass_editing| dispondremos de la configuración para la edición de varios registros.
Dispondremos en los modelos un nuevo asistente que nos permitirá hacer modificaciones para varios
registros a la vez.

La edición masiva nos permite añadir, editar o eliminar valores en los campos de los registros
seleccionados.

Esta funcionalidad es muy común por ejemplo en los casos de los productos. Poder seleccionar
varios productos a la vez y hacer una edición en todos ellos con el mismo valor.

.. |menu_mass_editing| tryref:: mass_editing.massediting_menu/complete_name

.. inheritref:: mass_editing/mass_editing:section:configuracion

Configuración
-------------

Los components que forman una Edición Masiva son:

* Un modelo con el que lo relacionamos
* Los campos que dispondremos en el asistente para editar

Para disponer del asistente en el modelo, para editar, debemos accionar el botón "Crear asistente".
Esto nos creará un nuevo asistente, disponible en el modelo.

El orden de los campos del asistente de edición seguirá el orden según el administrador vaya añadiendo
campos en la configuración de la "Edición masiva".

.. inheritref:: mass_editing/mass_editing:section:uso

Uso
---

Accionaremos el asistente o acción que disponemos en el modelo, en este asistente nos listarán todos
en los campos que se permiten hacer una edición.

En un campo dónde podamos editar podremos escoger las opciones:

* Establecer. Añade o modifica el campo
* Eliminar. Elimina el contenido del campo

Para los campos relacionados dispondremos de más opciones:

* Eliminar. Elimina la opción seleccionada
* Eliminar todos. Nos elimina todos los valores del campo.

Campos requeridos
-----------------

En el caso que seleccionemos la opción "Establecer" o "Eliminar" y no hayamos introducido un valor
a modificar, nos alertará con un mensaje en el campo requerido. Deberemos deseleccionar la opción si
no deseamos realizar ninguna tarea o rellenar un valor para ese campo.
