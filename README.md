# AudioToTextoIA
con el uso de wishper para transcribir audio a texto y gpt-4o para responder preguntas con dicho contexto de audio procesado

# Pasos de instalacion y ejecucion

1. accedemos a la carpeta de nuestro proyecto por medio de un terminal y ejecutamos el siguiente comando

    pip install -r recuariments.txt

    este comando instalara las librerias necesarias para poder correr nuestra aplicacion. 

2. agragamos el apikey a la clase Model.py y Transcriber.py, la linea en la que debe se bera de la siguiente manera.

    client = OpenAI(api_key="xxx")

    remplazamos las xxx por nuestra apikey de openAI necesario para que ejecute los modelos utilizados en esta palicacion.

3. ejecutamos el comando

    streamlit run index.py 

    donde podremos visualizar la url donde se estara ejecutando nuestra aplicaicon.
