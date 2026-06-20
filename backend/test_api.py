import base64
import requests

with open("test.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

response = requests.post(
    "http://127.0.0.1:5000/analyze",
    json={"image": image_base64}
)

print(response.status_code)
print(response.json())