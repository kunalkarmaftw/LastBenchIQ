# Tesseract is a SYSTEM binary, not a pip package. Deploying without it was
# identified in the Step 3 audit as a top-3 risk: tier-2 OCR silently fails and
# every scanned paper falls through to the paid vision fallback.
# A Dockerfile is how that binary gets onto the host.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        tesseract-ocr \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Verify at build time, not at 2am during the demo.
RUN tesseract --version && python -c "import sklearn, pandas, fitz, pytesseract"

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
