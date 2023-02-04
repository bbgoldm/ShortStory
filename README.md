# QR Code Microservice README

## Communication Contract

## How to REQUEST data:
- In order to REQUEST data from the QR code microservice, an HTTP POST request must be made to **port 5000** to the **'/qr-code'** endpoint.  The payload needs to contain a JSON object. 
- Here is an example call:
  - payload = {'cable_id': cable_id, 'cable_type': cable_type, 'install_date': my_date}
  - response = requests.post('http://localhost:5000/qr-code', json=payload)

## How to RECEIVE data:
- The microservice will return a base64-encoded string as a JSON response to the POST request.
- Create a URL that indicates the JSON is base64-encoded PNG.  The URL can be used as a src attribute to display the image.
- Here is example python code: 
  - image = response.json()['img']
  - src = 'data:image/png;base64,' + str(image)
  - return [html.Img(src=src)]
 
## UML sequence diagram showing how requesting and receiving data work. 

![image](https://user-images.githubusercontent.com/50001855/216782559-7ddb72dc-7992-42f1-a89f-0d3f4afb1cba.png)

