from kafka import KafkaProducer

def string_serializer(msg):
    return repr(msg).encode('utf-8')

def int_serializer(msg):
    return msg

def sendClientToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'client')
    print("Published client successfully")
    
def sendNameToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'name')
    print("Published Name successfully")
    
def sendBudgetToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'budget')
    print("Published Budget successfully")
    
def sendPeopleResourceToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'people')
    print("Published People Ressource successfully")

def sendDaysResourceToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'days')
    print("Published Days Ressource successfully")

def sendDeveloperToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'developer')
    print("Published Developers  successfully")

def sendQualityToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'quality')
    print("Published Quality  successfully")

def sendDevopsToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'devops')
    print("Published Devops  successfully")

def sendSupportToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'support')
    print("Published IT Support  successfully")

def sendDeliveryDateToTopic(data):
    producer = KafkaProducer(bootstrap_servers = 'localhost:9092',
                         value_serializer = string_serializer)
    producer.send("data-manager",data,key=b'deliveryDate')
    print("Published Delivery Date successfully")


