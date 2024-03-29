from fastapi import FastAPI
from app.routes.category_routes import router_category

app = FastAPI()

@app.get('/health-check')
def health_check():
    return True


app.include_router(router_category)
