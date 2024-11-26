import threading
import subprocess

def run_mqtt_test():
    subprocess.run(["python", "MQTT_Command.py"])

def run_streaming():
    subprocess.run(["python", "VideoStreaming.py"])

def run_sensor():
    subprocess.run(["python", "DistanceSensing.py"])

def run_buzzer():
    subprocess.run(["python", "Buzzer.py"])

if __name__ == "__main__":
    # MQTT 테스트 스레드 시작
    mqtt_thread = threading.Thread(target=run_mqtt_test)
    mqtt_thread.start()

    # MJPEG 스트리밍 스레드 시작
    streaming_thread = threading.Thread(target=run_streaming)
    streaming_thread.start()

    sensor_thread = threading.Thread(target=run_sensor)
    sensor_thread.start()
    
    buzzer_thread = threading.Thread(target=run_buzzer)
    buzzer_thread.start()
    
    # 메인 스레드에서 대기
    mqtt_thread.join()
    streaming_thread.join()
    sensor_thread.join()
    buzzer_thread.join()
