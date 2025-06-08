FROM python:3.10-slim


WORKDIR /app


COPY . /app


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    zbar-tools \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from models import init_db; init_db()"
RUN python populate_db.py


EXPOSE 5000


CMD ["flask", "run", "--host=0.0.0.0"]

