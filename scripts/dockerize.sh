docker rm -f $(docker ps -a -q --filter "ancestor=core-service")
echo "DOCKER IMAGE(s) UN-INSTALLED"

echo "building docker image"
docker build -t core-service ../.

if [ $? -eq 0 ]; then
    echo "RUNNING DOCKER IMAGE..."
    # add -d argument to run it in background
    # copy .env into image in local runs
    docker run --network=host -p 5000:5000 -v $(pwd)/../.env:/app/.env core-service:latest
else
    echo "Docker build failed. The container will not be run."
fi