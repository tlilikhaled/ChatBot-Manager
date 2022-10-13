from kafka import KafkaConsumer
import time
import json
global statut
def consumeMessage():
    time.sleep(30)
    consumer = KafkaConsumer(
        "notification-event",
        bootstrap_servers = 'localhost:9092',
        auto_offset_reset = 'earliest',
        group_id = "group_id",
        consumer_timeout_ms=10000
          
    )
    print("starting consume")
    for message in consumer:        
        aList = json.loads(message.value)
        statut = aList['content']
        return statut
    consumer.close()
    dispatcher.utter_message(text=f"{statut}")
        
        
    
    




