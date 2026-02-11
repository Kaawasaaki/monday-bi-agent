import requests
import pandas as pd
import streamlit as st

class MondayClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": self.api_key,
            "API-Version": "2024-01"  # Updated to the latest stable version
        }

    def fetch_board(self, board_id):
        # We use a simpler query first to see if we can just reach the board
        query = """
        query ($boardId: [ID!]) {
          boards (ids: $boardId) {
            name
            items_page (limit: 100) {
              items {
                name
                column_values {
                  text
                  column { title }
                }
              }
            }
          }
        }
        """
        variables = {'boardId': [str(board_id)]}
        
        try:
            response = requests.post(
                self.url, 
                json={'query': query, 'variables': variables}, 
                headers=self.headers
            )
            res_data = response.json()
            
            # This will print the REAL error in your VS Code terminal
            if "errors" in res_data:
                print(f"MONDAY API ERROR: {res_data['errors']}")
                return pd.DataFrame()
                
            board_data = res_data.get('data', {}).get('boards', [])
            if not board_data:
                print(f"No board found with ID: {board_id}")
                return pd.DataFrame()
                
            items = board_data[0]['items_page']['items']
            rows = []
            for item in items:
                row_dict = {'item_name': item['name']}
                for val in item['column_values']:
                    row_dict[val['column']['title']] = val['text']
                rows.append(row_dict)
                
            return pd.DataFrame(rows)
            
        except Exception as e:
            print(f"CONNECTION ERROR: {str(e)}")
            return pd.DataFrame()