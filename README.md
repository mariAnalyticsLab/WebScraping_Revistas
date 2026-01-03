# WebScraping_Revistas

## ✔️ Descripción del problema
En muchas plataformas de revistas científicas, los enlaces a los documentos PDF de los artículos no están disponibles de forma directa ni estructurada.
Estos enlaces suelen cargarse dinámicamente, aparecer después de realizar desplazamientos en la página o variar según la plataforma editorial.
Este script aborda el problema de extraer automáticamente las URLs de documentos PDF desde páginas de artículos científicos, como paso previo para la posterior extracción de correos electrónicos y ORCID.

## ⚠️ ¿Qué hace cada Script?
- WebScrapin_PDFs.py → Extrae URLs de PDFs
- WS_Correos.py → Extrae correos y ORCID desde PDFs y visores
- WS_Correos_Orcid.py → Extrae ORCID directamente desde páginas web


## ✔️ Funcionamiento
El script recibe un archivo CSV que contiene URLs de páginas de artículos científicos.
Para cada URL:
- Se abre la página utilizando Selenium en modo headless.
- Se realiza un desplazamiento automático hasta el final de la página para asegurar que todo el contenido dinámico se cargue correctamente.
- Se buscan enlaces a PDFs utilizando múltiples selectores HTML y XPath, adaptándose a distintas estructuras editoriales.
- Los enlaces detectados se almacenan temporalmente.
- El proceso se ejecuta de forma paralela utilizando ThreadPoolExecutor para mejorar el rendimiento.
- Se utiliza un mecanismo de bloqueo (Lock) para evitar conflictos al consolidar los resultados.
- Finalmente, todas las URLs de PDFs encontradas se guardan en un archivo CSV.

## ✔️ Herramientas y tecnologías utilizadas
- Python 3
- Selenium WebDriver
- Google Chrome (modo headless)
Librerías
- selenium
- pandas
- threading
- concurrent.futures
- time
- os
- urllib3
- csv
- VisualStudioCode

## ✔️ Datos
- Este repositorio no incluye URLs reales de artículos ni documentos PDF.
- Los archivos de entrada y salida pueden contener enlaces a documentos de acceso público, pero no se publican por razones éticas y de privacidad.

## ✔️ Resultados y aprendizajes obtenidos
- Extracción automatizada de enlaces a documentos PDF desde páginas web dinámicas.
- Identificación de múltiples patrones HTML usados por distintas revistas científicas.
- Uso de desplazamiento automático para asegurar la carga completa del contenido.
- Implementación de concurrencia para reducir tiempos de ejecución.
- Integración efectiva de scraping web como paso previo a procesos de análisis documental.
- Consolidación y eliminación implícita de duplicados.

## ✔️ Limitaciones
- Cambios en la estructura HTML de los sitios pueden afectar la detección de enlaces.
- Algunos artículos no ofrecen acceso al PDF.
- El rendimiento depende del tiempo de carga y estabilidad de cada sitio.
- El uso de Selenium puede ser costoso en recursos computacionales.
- El scraping puede estar sujeto a restricciones impuestas por las plataformas visitadas.

## ✔️ Disclaimer
Este script automatiza la navegación en sitios web de acceso público con fines educativos y de investigación.
El usuario es responsable de respetar los términos de uso de cada plataforma y la normativa vigente en materia de protección de datos.

