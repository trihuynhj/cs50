# HTTP REQUEST TEST (PYTHON'S REQUESTS MODULE)

import requests

x1 = requests.get("https://vnexpress.net/ha-noi-dung-hoat-dong-22-chot-kiem-soat-cua-ngo-thu-do-437459aefawefew").status_code
x2 = requests.get("https://vnexpress.net/ha-noi-dung-hoat-dong-22-chot-kiem-soat-cua-ngo-thu-do-4374598.html").status_code

print(x1)
print(x2)