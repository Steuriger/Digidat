# Verwenden Sie ein Basisimage, das <link>Python</link> enthält
FROM python:3.8-slim

# Legen Sie das Arbeitsverzeichnis im Container fest
WORKDIR /app

# Kopieren Sie die Datei "requirements.txt" in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren Sie die erforderlichen <link>Python</link>-Abhängigkeiten
RUN pip install -r requirements.txt

# Kopieren Sie den gesamten Inhalt des lokalen "<link>Python</link>" -Ordners in das Arbeitsverzeichnis im Container
COPY Python/ .

# Starten Sie die Anwendung, wenn der Container ausgeführt wird
CMD [ "python", "app.py" ]