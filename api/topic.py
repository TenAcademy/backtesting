from kafka.admin import KafkaAdminClient, NewTopic

def create_topic(topics:list,bootstrap_servers=['b-1.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092',
        'b-2.batch6w7.6qsgnf.c19.kafka.us-east-1.amazonaws.com:9092']):
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers
    )

    topic_list = []
    for topic in topics:
        topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
        
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
