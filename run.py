import gui_app
import flet as ft

def main(page):
    app = gui_app.ScraperApp(page)

if __name__ == "__main__":
    ft.app(target=main)


# tested on: 
# https://www.jobs.cz/rpd/2000147251/?searchId=c2227d40-dc5b-47f1-b6bd-37a9caefcdd4&rps=233
# https://www.jobs.cz/fp/asb-czech-republic-s-r-o-233975/2000176507/?searchId=5b2e93b9-305a-443a-87dd-e647bfdf8e7c&rps=329 
