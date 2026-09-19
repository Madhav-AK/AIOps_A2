AI OPs Assignment 2 Submission
- By Madhav AK
- DA24B012

This README file goes through all major submission points.

- Main 2 pg report can be found in the main directory of this report.
- Video Submission Link: 
- Questionwise folders have been created

### Questions 1 and 2

```bash
cd q1-q2

docker build -f Dockerfile_naive -t a2-spam-naive .
docker build -f Dockerfile_multi -t a2-spam-multi .
docker images

docker run -d --name spam-naive -p 8080:8080 a2-spam-naive:latest
curl http://localhost:8080/healthz; echo
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"WIN a FREE laptop now!"}'; echo
docker stop spam-naive

docker run -d --name spam-multi -p 8080:8080 a2-spam-multi:latest
curl http://localhost:8080/healthz; echo
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"WIN a FREE laptop now!"}'; echo
docker stop spam-multi

docker compose build
docker compose up -d
docker compose ps

# Run twice, one for miss, next for hit 
curl -s -w '\nTime taken for command: %{time_total}s\n' \
  http://localhost:8080/predict \
  -H 'Content-Type: application/json' \
  -d '{"text":"WIN a FREE laptop now! Evidence test 001"}'

curl -s -w '\nTime taken for command: %{time_total}s\n' \
  http://localhost:8080/predict \
  -H 'Content-Type: application/json' \
  -d '{"text":"WIN a FREE laptop now! Evidence test 001"}'

docker compose down
```

### Question 3

```bash
cd q3

minikube start -p a2-cluster --nodes=2 --cpus=2
kubectl --context=a2-cluster get nodes -o wide

docker build -t email-validator-worker:v2 .
minikube image load email-validator-worker:v2 -p a2-cluster

kubectl --context=a2-cluster delete job email-validator-job --wait=true
kubectl --context=a2-cluster apply -f job-single-node.yml

# Run this command to see status:
kubectl --context=a2-cluster get pods \
  -l job-name=email-validator-job -o wide

kubectl --context=a2-cluster get job email-validator-job

kubectl --context=a2-cluster logs \
  -l job-name=email-validator-job --prefix=true --tail=-1 \
  | tee q3-validation-results.txt
grep -E 'Shard:|Invalid rows:' q3-validation-results.txt
```

### Question 4

```bash
cd q4
minikube start

# Set APP_VERSION="v1" in predictor.py to re-do the roll back for yourself. deployment.yaml uses a2-spam-q4:v1. (Currently the latest version of the repo has v2 on it)
docker build -t a2-spam-q4:v1 .
minikube image load a2-spam-q4:v1
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

kubectl get deployments
kubectl get pods
kubectl get service
minikube service spam-predictor-svc --url # Assuming the url returned was: http://192.168.49.2:30080.

curl http://192.168.49.2:30080/healthz
curl -X POST http://192.168.49.2:30080/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"WIN a FREE iPhone now! Click here: bit.ly/xyz123"}'

kubectl get pods
kubectl delete pod <pod-name> # Replace <pod-name> with a pod shown by kubectl get pods.
kubectl get pods

# Now you'll need to change APP_VERSION from "v1" to "v2" in predictor.py.

docker build -t a2-spam-q4:v2 .
minikube image load a2-spam-q4:v2
kubectl set image deployment/spam-predictor predictor=a2-spam-q4:v2
kubectl rollout status deployment/spam-predictor
kubectl rollout history deployment/spam-predictor
kubectl get pods
curl http://192.168.49.2:30080/healthz
```
