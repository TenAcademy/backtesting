from kafka import KafkaProducer

def produce(topic:str,message:str,bootstrap_servers:list=['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092','b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092']):
    """
    Produce: 
        Method
    Accepts:
        Topic : str -  a topic the message is produced to
        message : str - the message wanted to produced
        bootstrap_servers : list - list of bootstrap servers you want to connec

        return nothing 
    """
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    
    msg = bytes(f"{message}", encoding='utf-8')
    producer.send(topic, msg)
    producer.flush()

    print("Produced!")
    