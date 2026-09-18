docker build -f Dockerfile_naive -t a2-spam-naive .
docker build -f Dockerfile_multi -t a2-spam-multi .


docker run --name spam-naive -p 8080:8080 a2-spam-naive:latest
docker run --name spam-multi -p 8080:8080 a2-spam-multi:latest

curl http://localhost:8080/healthz; echo

curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"text":"WIN a FREE laptop now!"}'; echo



docker compose build
docker compose up -d

curl -s -w '\nTime taken for command: %{time_total}s\n' \
  http://localhost:8080/predict \
  -H 'Content-Type: application/json' \
  -d '{"text":"WIN a FREE laptop now! Evidence test 001"}'