# NEXO para iPadOS

Este directorio contiene el proyecto de aplicación iOS de NEXO. La interfaz web existente se copia dentro del paquete de la aplicación, por lo que la app no necesita abrir Safari ni descargar la interfaz desde GitHub Pages.

## Compilación automática

El workflow `.github/workflows/build-ios.yml` compila el proyecto en un runner macOS y publica un artefacto para revisar el resultado.

## Instalación en un iPad

GitHub puede compilar el proyecto, pero no puede instalar una app en tu iPad por sí solo. Para instalar una app iOS en un dispositivo real hace falta firmarla con una identidad de desarrollo y un perfil de aprovisionamiento compatibles con ese iPad. No se debe publicar una clave privada ni un certificado en el repositorio.

La compilación automatizada inicial no está firmada y sirve para validar el proyecto. Antes de usarla en el iPad habrá que configurar la firma de forma segura. La cuenta gratuita de Apple permite pruebas personales mediante Xcode, con limitaciones de caducidad; la distribución persistente requiere revisar las opciones actuales de Apple.

## Datos

La interfaz actual conserva datos en el almacenamiento web del dispositivo. Antes de usar la app como única copia de tus tareas, prueba crear una tarea, cerrar la app y volver a abrirla. No borres los datos de la PWA anterior hasta verificar que todo se conserva en la nueva app.
