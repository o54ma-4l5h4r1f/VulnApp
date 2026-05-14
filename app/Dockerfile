FROM python:3.9

WORKDIR /app

# VULN-6: COPY . . includes .env, .git, private keys — use .dockerignore
COPY . .

RUN pip install --no-cache-dir -r app/requirements.txt

# VULN-7: Secret baked into image layer — visible via docker history
ENV API_SECRET_KEY="sk-prod-bakedintoimage-never-do-this"

# VULN-8: No USER directive — container runs as root
EXPOSE 5000

CMD ["python", "app/app.py"]