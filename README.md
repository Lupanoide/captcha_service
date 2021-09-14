

Per testare il servizio:

# Creare l'immagine:

docker build -t "captcha_service:1.0" .

### Farla girare. I servizi saranno esposti sulla porta 8000 . Per evitare di dover montare volumi esterni mi sono appoggiato a sqlite come db
### per memorizzare le stringhe generate.Ho creato uno scheduler che ogni 180 secondi cancella le stringhe generate rendendole obsolete

docker run -p 8000:8000 "captcha_service:1.0"

# GET API
### L'endpoint da interrogare è /get_captcha. Il servizio restituisce l'immagine codificata come bytes. Ho utilizzato pillow per produrre l'immagine
### e la consiglio per aprire l'immagine restituita

from PIL import Image
import requests
import io


r = requests.get("http://localhost:8000/get_captcha")
stream = io.BytesIO(r.content)
image = Image.open(stream)
image.show()


# POST API
### è una api json con un solo argomento solution a cui bisogna accoppiare la stringa letta nell'immagine precedente. L'endpoint è /validate_captcha 

r1 = requests.post("http://localhost:8000/validate_captcha",json={"solution":"pyv2lp6qu"})
r1.text

