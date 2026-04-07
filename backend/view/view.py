from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="backend/view/templates")


class View:
    def get_index_view(self, request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
