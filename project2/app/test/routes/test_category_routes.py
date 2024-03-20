from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

from app.db.models import Category as CategoryModel
from app.schemas.category import CategoryOutput
from app.use_cases.category import CategoryUseCases

client = TestClient(app)


def test_add_category_route(db_session):
    body = {
        "name": "Roupa",
        "slug": "roupa",
    }
    
    response = client.post('/category/add/', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    categories_on_db = db_session.query(CategoryModel).all()
    assert len(categories_on_db) == 1
    db_session.delete(categories_on_db[0])
    db_session.commit()


def test_list_categories(db_session, categories_on_db):
    uc = CategoryUseCases(db_session=db_session)

    categories = uc.list_categories()

    assert len(categories) == 4
    assert type(categories[0]) == CategoryOutput
    assert categories[0].id == categories_on_db[0].id
    assert categories[0].name == categories_on_db[0].name
    assert categories[0].slug == categories_on_db[0].slug
