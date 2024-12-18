# Realtime chat!

# Setup
Requirements:
-   docker
-   python

Steps:
```
# 1. Check the environment variables and change variables if required

# 2. Run the stack
docker-compose up

# 3. run or follow the different steps
chmod +x 1-docker-cert.sh
./1-docker-cert.sh

# 4. Python requirements
pip install -r python/requirements
```

Open index.html to see relevant links such as kibana: http://localhost:5601/login

# Run
```
python python/ingest_characters.py
python chat.py
python autocompletion.py
```
