# EDA - Event Driven Architecture with Python, FastAPI and Kafka

This educational repo adopts event driven architecture in python, fastapi and kafka.

### How to Test

1- Get your local kafka up as

```shell
cd scripts
./dependencies.sh
```

You will be able to access kafka-ui at http://localhost:8080/

2- Get the service up in a different terminal as

```shell
cd scripts
./service.sh
```

You will be able to access the home page of the service at http://localhost:5000/

3- Perform a test as

```shell
curl -X POST http://localhost:5000/analyze \
    -H "Content-Type: application/json" \
    -d '{"image": "https://raw.githubusercontent.com/serengil/retinaface/refs/heads/master/tests/dataset/img3.jpg"}'
```

### In Summary

This service processes the provided image in the background. First, it detects and extracts faces from the image. Next, each extracted face is sent to the Kafka topic `faces.extracted`. Finally, messages from this topic are consumed and analyzed in parallel to predict facial attributes such as age and gender using DeepFace.

The number of workers can be configured via the workers argument in service.sh. Best practices recommend aligning the number of workers with the number of Kafka partitions. For example, we created a Kafka topic with 8 partitions but limited the Flask server to 2 workers. For production, it’s recommended to keep these numbers consistent. Additionally, you can increase both the number of partitions and workers in the configuration to make the system highly scalable.

While a threading or multiprocessing approach would be limited by the number of cores on a single machine, this event-driven architecture allows scaling across multiple machines efficiently.