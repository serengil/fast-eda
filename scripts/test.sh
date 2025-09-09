curl -X POST http://localhost:5000/analyze \
    -H "Content-Type: application/json" \
    -d '{"image": "https://raw.githubusercontent.com/serengil/retinaface/refs/heads/master/tests/dataset/img3.jpg"}'