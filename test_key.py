import requests
token = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYxOTgzNjkzMywiYWFpIjoxMSwidWlkIjo5OTcwNjExOSwiaWFkIjoiMjAyNi0wMi0xMVQwNjoyODoxNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MzM3NDgzMjIsInJnbiI6ImFwc2UyIn0.MaI59P9gXZrUcxJJw1cms8_sIB5P8BMeg-Og6_lziy4'
url = "https://api.monday.com/v2"
headers = {"Authorization": token, "API-Version": "2024-01"}
query = "{ me { name } }"
response = requests.post(url, json={'query': query}, headers=headers)
print(response.json())