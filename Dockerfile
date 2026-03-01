# استخدام نسخة بايثون خفيفة
FROM python:3.9

# تحديد مكان العمل جوه السيرفر
WORKDIR /code

# نسخ ملف المكتبات وتسطيبها
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تشغيل السيرفر على بورت 7860 (ده بورت Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
