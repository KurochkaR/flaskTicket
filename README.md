1. Create database on postgres tickets
2. Rename .env2 to .env
3. Run docker compose up --build
4. Run docker exec -it flask-ticket flask db migrate
5. Run docker exec -it flask-ticket flask db upgrade
6. Open http://localhost:5005/
