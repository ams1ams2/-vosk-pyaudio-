import time
import pyaudio
import wave
import json
from vosk import Model, KaldiRecognizer

# تحميل النموذج
model = Model("vosk-model-ar-0.22-linto-1.1.0")

# تهيئة الميكروفون
p = pyaudio.PyAudio()

# إعداد البث من الميكروفون (Input Stream)
stream = p.open(format=pyaudio.paInt16,  # تنسيق الصوت
                channels=1,              # قناة واحدة (أحادي)
                rate=16000,              # معدل أخذ العينات (16 كيلو هرتز مناسب للـ Vosk)
                input=True,              # نختار الميكروفون كمدخل
                frames_per_buffer=4000)   # عدد الإطارات لكل طلب

# تهيئة التعرف على الكلام
rec = KaldiRecognizer(model, 16000)

print("ابدأ التحدث...")

# التقاط وتحويل الصوت في الوقت الفعلي
try:
    while True:
        # التقاط البيانات من الميكروفون
        data = stream.read(4000)
        if rec.AcceptWaveform(data):
            # إذا تم قبول الموجة، طباعة النتيجة
            print(rec.Result())
            time.sleep(1)

        else:
            # إذا لم يتم قبول الموجة بعد، الاستمرار في المعالجة الجزئية
            print(rec.PartialResult())
except KeyboardInterrupt:
    # إيقاف التسجيل عند الضغط على Ctrl+C
    print("\nتم إيقاف التسجيل.")
finally:
    # إغلاق الميكروفون بشكل صحيح
    stream.stop_stream()
    stream.close()
    p.terminate()

    # طباعة النتيجة النهائية
    print(rec.FinalResult())
