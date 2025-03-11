FROM python:3.8-slim

ENV TZ="Atlantic/Cape_Verde"

RUN pip install --no-cache-dir \
    urllib3==1.26.6 \
    snips-nlu \
    fastapi \
    uvicorn


COPY utils.py /usr/local/lib/python3.8/site-packages/snips_nlu/cli/utils.py

RUN pip config set global.trusted-host "resources.snips.ai" --trusted-host=https://resources.snips.ai/

RUN python -m snips_nlu download-language-entities pt_pt
RUN python -m snips_nlu download-language-entities en

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN printf "float = float\nint = int" >> /usr/local/lib/python3.8/site-packages/numpy/__init__.py

VOLUME ["/app/features/version_controller"]

EXPOSE 1178

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1178"]

