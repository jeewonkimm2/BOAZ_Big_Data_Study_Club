# <목표>

<img width="830" alt="Screenshot 2023-02-25 at 6 18 10 PM" src="https://user-images.githubusercontent.com/108987773/221349170-30b7cd59-0a8b-40f2-8a60-7388c0fc57e1.png">

- Stream Serving을 구현하기 위하여 Kafka를 이용하여 데이트 파이프라인 구축
- Kafka를 이용하여 Source DB(데이터가 계속해서 쌓이고 있는 외부 DB) 서버에 있는 데이터를 Target DB(외부에서 가져온 데이터를 처리한 뒤 쌓이는 내부 DB)로 전달하는 시스템 구축
---
# <1> Kafka Introduction
1. 메세징 시스템

<img width="823" alt="Screenshot 2023-02-25 at 6 22 08 PM" src="https://user-images.githubusercontent.com/108987773/221349359-e1bf4d63-6360-4023-83fe-0952292612aa.png">

- 메세징 시스템 (Message System)
  - 서로 다른 어플리케이션끼리 정보를 교환하기 위해 메세지의 생성, 전송, 전달 및 저장을 가능하게 하는 시스템
  - 주로 하나의 어플리케이션이 외부 하나 이상의 데이터 소스로부터 데이터를 받는 어플리케이션에 의해 처리된 데이터를 전달받고 싶을 때 사용
  - 메세지 : 하나의 entity에서 다른 하나의 entity로 정보를 전송하는 데 사용되는 통신 artifact
  - 대표적인 시스템 : Kafka, RabbitMQ, Active MQ, AWS SQS, Java JMS 등
  - 장점

    <img width="822" alt="Screenshot 2023-02-25 at 6 37 39 PM" src="https://user-images.githubusercontent.com/108987773/221350152-456890bb-7bc6-46a9-b6fa-50904ec03f10.png">
    
    - 메세지 생산자(message producer)와 메세지 소비자(message consumers) 사이에 약한 결합성(loose coupling)을 갖도록 함. 약한 결합성이란 한 쪽이 끊기거나 변경이 있어도 다른 쪽에 미치는 영향이 작은 것.
    - 메시지 생산자와 소비자는 서로 알지 못함 -> 동적이고, 신뢰성 있고 유연한 시스템을 구현할 수 있도록 해주며, 그에 따라 시스템의 나머지 부분에 영향을 주지 않고 하위 어플리케이션의 전체적인 구성을 변경할 수 있음.
    - 높은 확장성과 서로 다른 네트워크 사이의 쉬운 통합성과 안정성
  - 용어 정리
    - Message Oriented Middleware (MOM)
      - 독립된 어플리케이션 간에 데이터를 주고받을 수 있도록 하는 시스템 디자인 : 함수 호출, 공유메모리 등의 방식이 아닌, 메세지 교환을 이용하는 중간 계층에 대한 인프라 아키텍처 / 분산 컴퓨팅이 가능해지며, 서비스간의 결합성이 낮아짐
      - 비동기 (asynchronous) 로 메시지를 전달
      - Queue, Broadcast, Multicast 등의 방식으로 메세지를 전달
      - Publish/Subscribe (Pub/Sub) 구조 : 메시지를 발행하는 Publisher, 메시지를 소비하는 Subscriber 로 구성
    - Message Broker
      - 메시지 처리 또는 메시지 수신자에게 메시지를 전달하는 시스템이며, 일반적으로 MOM을 기반으로 구축
    - Message Queue(MQ)
      - Message Broker와 MOM을 구현한 소프트웨어 (Kafka, RabbitMQ, ActiveMQ 등)
    - Advanced Message Queueing Protocol(AMQP)
      - 메시지를 안정적으로 주고받기 위한 인터넷 프로토콜
      - MOM은 메시지 전송 보장을 해야하므로 AMQP를 구현

2. Kafka
- Open-source Distributed Event Streaming Platform. 발생하는 데이터를 실시간으로 처리하고, 필요에 따라서 데이터가 또 다른 target 시스템으로 event stream 을 라우팅 해주는 것.
- 특징
  1. Event Streaming Platform : Event Stream을 실시간으로 처리하고 계속 쌓이는 데이터를 지속적으로 보관하다가 그 데이터를 쓰려고 하는 다른 target 시스템들이 가져갈 수 있도록 제공
  2. Publish/Subscribe (Pub/Sub) 구조 : 다른 시스템에서 데이터를 가져와서 Kafka 에 publish (발행, 저장)하거나 Kafka 로부터 데이터를 subscribe (구독, 읽기) 할 수 있는 기능을 제공
  3. Decoupling : Kafka 에서는 Pub/Sub 구조를 구현하기 위해 Producer(Kafka 에 event 를 publish 하는 client application) 와 Consumer(Kafka 로부터 event 를 subscribe 하는 client application) 가 존재합니다. 두 객체는 서로 의존적이지 않고 완벽하게 분리
- 아키텍처
  
  <img width="832" alt="Screenshot 2023-02-25 at 7 01 43 PM" src="https://user-images.githubusercontent.com/108987773/221351068-6829f7af-1574-4200-804e-2b6b3bbc7420.png">

- 컴포넌트
  1. Broker
    - 브로커 (Broker) 란 메시징 서비스를 담당해주는 Kafka 서버 또는 Kafka 시스템
    - 하나의 브로커 == 하나의 Kafka Broker Process
    - 클러스터를 구성할때 주로 다중 브로커를 사용. 브로커가 여러 개일 경우, 각각의 브로커들은 ID로 식별
    - 역할 : 토픽 (Topic) 내의 파티션 (Partition) 들의 분산, 유지 및 관리
    - 토픽의 일부 파티션들을 포함하고 있지만, 데이터의 일부분인 파티션을 갖을 뿐 전체 데이터를 갖고 있지는 않음
  2. Cluster
    - Kafka 클러스터 (Cluster) 는 여러 개의 브로커로 이루어진 집합체. 일반적으로 최소 3대 이상의 브로커를 하나의 클러스터로 구성
  3. Topic
    - 토픽 (Topic) 이란 브로커에서 event (data) 를 관리하는 “기준” 또는 어떤 event 를 저장할 지를 정하는 “주제”
    - 토픽은 파일 시스템의 “폴더” 와 같고, event 는 폴더 속의 “파일” 과 같음. 전통적인 메시징 시스템과는 다르게 message (event) 들을 subscribe 해서 받아보더라도 그 메시지는 삭제되지는 않음
    - 대신 토픽마다 지정된 기준에 따라 event 를 유지할 지 정할 수 있는데, 이 때 설정된 기간 또는 용량에 따라 event 를 유지
   4. Partition
    - 토픽에는 파티션 (Partition) 이 존재하며 모든 파티션들은 Producer 로부터 전달된 데이터를 보관하는 역할
    - 반드시 존재하는 리더 파티션 (Leader Partition) 과 존재할 수도 있는 팔로워 파티션 (Follower Partition) 으로 구분
      - 리더 파티션 : Producer 또는 Consumer 와 직접 통신하는 파티션 / Producer 또는 Consumer 와 직접 통신함으로써 read 와 write 연산을 담당
      - 팔로워 파티션 : Producer 에 의해 리더 파티션으로 전달된 데이터를 복제하여 저장 / 팔로워 파티션의 가장 중요한 역할은 리더 파티션의 데이터를 복사하여 보관하는 역할을 하고 있다가 리더 파티션이 속해있는 브로커에 장애가 발생하면, 팔로워 파티션이 리더 파티션의 지위를 가지게 됨
    5. Zookeeper
      - 분산 시스템에서 시스템 간의 정보 유지, 상태 체크, 서버들 간의 동기화 등을 처리해주는 분산 코디네이션 서비스 (Distributed Coordination Service)
      -  직접 어플리케이션 작업을 조율하지 않고, 조율하는 것을 쉽게 개발할 수 있도록 도와줌
      -  API 를 이용하여 동기화를 하거나 마스터 선출 등의 작업을 쉽게 구현
      -  주키퍼의 데이터는 분산 작업을 제어하기 위해 트리 형태의 데이터 저장소에 스냅샷을 저장
      -  주키퍼 앙상블 (Zookeeper Ensemble) 이란 주키퍼 서버의 클러스터. 하나의 주키퍼 서버에 문제가 생겼을 경우, 주키퍼 서버들에 쌓이는 데이터를 기준으로 일관성을 맞추기 때문에 클러스터는 보통 홀수로 구축하며 최소 3개로 구축해야하며 일반적인 경우라면 5개를 권장
      -  파티션처럼 하나의 리더 서버가 있고, write 를 담당합니다. 그리고 나머지 팔로워 서버가 있고, read 를 담당
    6. Producer & Consumer
      - Producer : "메시지를 생산" 해서 브로커의 토픽으로 메시지를 보내는 역할을 하는 어플리케이션 또는 서버
        - 데이터를 전송할 때 리더 파티션을 가지고 있는 브로커와 직접 통신
        - 원하는 토픽의 파티션에 전송만하며 이후에 어떤 Consumer 에게 전송되는 지는 신경쓰지 않음
      - Consumer : 토픽의 파티션에 저장되어 있는 "메시지를 소비" 하는 역할을 하는 어플리케이션 또는 서버
        - 데이터를 요청할 때 리더 파티션을 가지고 있는 브로커와 통신하여 토픽의 파티션으로부터 데이터를 가져감
        - Consumer 의 운영 방법은 2가지
          - 토픽의 특정 파티션만 구독하는 Consumer 를 운영
          - 1개 이상의 Consumer 로 이루어진 Consumer 그룹을 운영
        - Consumer 역시 어떤 Producer 에게서 메시지가 왔는지는 관심이 없고, 원하는 토픽의 파티션을 읽어서 필요한 메시지만 받음
---
# <2> Producer & Consumer

1. Zookeeper & Broker Setup
- Docker Compose 작성 : [naive-docker-compose.yaml][link]
  - ZOOKEEPER_SERVER_ID : 주키퍼 클러스터에서 해당 주키퍼를 식별할 ID 를 지정. 이번 챕터에서는 ID 를 1로 지정
  - ZOOKEEPER_CLIENT_PORT : 주키퍼 client 의 포트를 지정. 이번 챕터에서는 기본 주키퍼의 포트인 2181 로 지정
  - KAFKA_SERVER_ID : 브로커의 ID 를 지정.  단일 브로커에서는 없어도 무방하나 이번 챕터에서는 1 로 지정
  - KAFKA_ZOOKEEPER_CONNECT : 브로커가 주키퍼에 연결하기 위한 주소를 지정. 일반적으로 ```주키퍼 서비스 이름 : 주피커 서비스 포트``` 형식으로 작성. 앞서 띄운 주키퍼의 이름과 포트인 zookeeper:2181 를 입력
  - KAFKA_ADVERTISED_LISTENERS : 내부와 외부에서 접속하기 위한 리스너를 설정. 일반적으로 internal 과 external 를 같이 설정하며, ```,``` 로 연결해서 작성. 이번 챕터에서는 internal 로 ```PLAINTEXT://broker:29092``` 로 설정하고, external 로 ```PLAINTEXT_HOST://localhost:9092``` 으로 설정. 최종적으로 ```PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092``` 를 입력
  - KAFKA_LISTENER_SECURITY_PROTOCOL_MAP : 보안을 위한 protocol mapping 을 설정. 이 설정값은 KAFKA_ADVERTISED_LISTENERS 과 함께 key/value 로 매핑. 이번 챕터에서는 ```PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT``` 로 설정
  - KAFKA_INTER_BROKER_LISTENER_NAME : 컨테이너 내부에서 사용할 리스너 이름을 지정. 이번 챕터에서는 앞서 internal 로 설정했던 ```PLAINTEXT``` 를 입력
  - KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR : 토픽을 분산하여 저장할 Replication Factor 를 설정. 이번 챕터에서는 단일 브로커를 사용하기 때문에 ```1``` 로 지정
  - KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS : 카프카 클러스터에서 초기에 rebalancing 할 때 Consumer 들이 Consumer group 에 조인할 때 대기하는 시간. 이번 챕터에서는 ```0``` 으로 설정
- 실행

  ```
  docker compose -p part7-naive -f naive-docker-compose.yaml up -d
  ```
  
- 결과

  <img width="1140" alt="Screenshot 2023-02-27 at 8 07 07 PM" src="https://user-images.githubusercontent.com/108987773/221548003-d7ecf067-22e8-4a03-8ba0-7e9a1860a121.png">

  <img width="800" alt="Screenshot 2023-02-27 at 8 07 29 PM" src="https://user-images.githubusercontent.com/108987773/221548093-4e210536-2cab-4cbb-b4e9-fd5aaf9c43fd.png">

2. Producer & Consumer Setup

- ```topic-test```라는 이름의 topic 생성

  ```
  docker compose -p part7-naive exec broker kafka-topics --create --topic topic-test --bootstrap-server broker:29092 --partitions 1 --replication-factor 1
  ```
  
  - 결과
  
    <img width="1154" alt="Screenshot 2023-02-27 at 8 16 52 PM" src="https://user-images.githubusercontent.com/108987773/221550013-aa55af2a-cec8-46ca-8497-3f9c51bd9213.png">

- Topic 생성 결과 확인

  ```
  docker compose -p part7-naive exec broker kafka-topics --describe --topic topic-test --bootstrap-server broker:29092
  ```
  
  - 결과
  
    <img width="1153" alt="Screenshot 2023-02-27 at 8 18 14 PM" src="https://user-images.githubusercontent.com/108987773/221550269-dd4e8369-c452-4b06-80d7-e85a8de6de17.png">

- Topic 을 사용할 Consumer 만들기
  - Broker Container 접속
  
    ```
    docker compose -p part7-naive exec broker /bin/bash
    ```
    
  - 결과

    <img width="668" alt="Screenshot 2023-02-27 at 8 19 52 PM" src="https://user-images.githubusercontent.com/108987773/221550621-151b9a32-380a-4aa3-9955-0fd4ad98fc84.png">

  - ```topic-test``` 토픽을 subscribe
    - 실행
    
      ```
      kafka-console-consumer --topic topic-test --bootstrap-server broker:29092
      ```
      
    - 결과
    
      <img width="702" alt="Screenshot 2023-02-27 at 8 23 22 PM" src="https://user-images.githubusercontent.com/108987773/221551351-aef17bca-dd67-4a75-a77f-78e9c455aded.png">
      
        -  수신을 대기하고 있는 상태가 됨
        
- Producer 를 만들어서 메시지를 보낼 준비
  ```
  주의 사항!
  
  새로운 터미널 창에서 실행
  ```
  - Broker Container 접속
  
    ```
    docker compose -p part7-naive exec broker /bin/bash
    ```
  
  - ```topic-test``` 토픽에 접근하여 publish 할 준비
  
    ```
    kafka-console-producer --topic topic-test --broker-list broker:29092
    ```
    
    - 결과
    
      <img width="669" alt="Screenshot 2023-02-27 at 8 26 31 PM" src="https://user-images.githubusercontent.com/108987773/221552034-71d5daa7-f5a7-48fe-8b86-7804d4427979.png">
      
- 최종 결과

  <img width="671" alt="Screenshot 2023-02-27 at 8 27 35 PM" src="https://user-images.githubusercontent.com/108987773/221552250-5677ea82-d7eb-4e54-b186-18f28dce3218.png">
  
  - Producer (메시지 발신)
  
  <img width="727" alt="Screenshot 2023-02-27 at 8 27 51 PM" src="https://user-images.githubusercontent.com/108987773/221552306-099b818e-70a2-4568-85e8-6c744f9c4781.png">
  
  - Consumer (메시지 수신)

- Zookeeper와 Broker 종료

  ```
  docker compose -p part7-naive down -v
  ```
---
# <3> Connect & Connector

1. Producer & Consumer의 한계

<img width="839" alt="Screenshot 2023-02-27 at 8 31 11 PM" src="https://user-images.githubusercontent.com/108987773/221552964-8b6888ba-bb64-4786-b7fc-831dca37dffb.png">

- DB server 1로부터 데이터를 가져오는 Producer 가 있고, 데이터를 브로커의 어떤 토픽으로 보낸 뒤, Consumer 가 DB server 2에 데이터를 전달하는 과정
- 이렇게 전달할 DB 들이 100개, 1000개, 10000개가 있다면 어떨까? 메시지 파이프라인 구성을 위해 매번 Producer 와 Consumer 를 개발하는 것은 쉽지 않음. 특히, 비슷한 데이터 시스템이 많아지면 많아질수록 Producer 와 Consumer 를 개발하는 데에는 비용도 계속 들고 반복 작업이 많아질 수 있음
- 따라서, 더 간편하고 효율적으로 메시지 파이프라인을 구축하는 방법으로 Kafka 에서는 Connect 와 Connector 라는 것이 탄생하게 되었음

2. Connect & Connector 소개

- Connect : 데이터 시스템과 Kafka 간의 데이터를 확장 가능하고, 안전한 방법으로 streaming 하기 위한 도구
- Connector : 데이터를 어디로부터 가져오는지, 어디에다가 전달해야 하는지를 알려주는 Connector 를 정의해야 Connect을 사용할 수 있음. Connector 란 메시지 파이프라인에 대한 추상 객체이며, task 들을 관리
  - Source Connector : Source system 의 데이터를 브로커의 토픽으로 publish 하는 Connector(Producer 의 역할을 하는 Connector)
  - Sink Connector : 브로커의 토픽에 있는 데이터를 subscribe 해서 target system 에 전달하는 Connector(Consumer 의 역할을 하는 Connector)
- Connect 는 프레임워크, Connector 는 그 안에서 돌아가는 플러그인. 따라서 Connect 프레임워크를 실행하고 특정 Connector 플러그인을 실행시키면 메시지 파이프라인을 쉽게 구축할 수 있음. 이렇게 구축된 Connect 와 Connector 를 실행함으로써 개발 비용을 줄이고 반복 작업도 줄일 수 있음
- 각각의 Connector 에 관한 설정 명세를 Connect 에 전달하면, 구성된 Connector 는 주기적으로 메시지를 확인하고 새로운 메시지가 있으면 파이프라인을 통해 흘려보냄

  <img width="823" alt="Screenshot 2023-02-27 at 8 36 47 PM" src="https://user-images.githubusercontent.com/108987773/221554022-e8992289-6b5c-4ea1-adb7-cc6d6b2b3cc1.png">

- 장점 : Connector 에 대한 설정파일만 있으면 개발 비용 없이 간단하게 띄울 수 있다는 것
     
3. Schema Registry 소개
- Connect와 함께 쓰이는 Schema Registry
- Kafka 는 decoupling 이라는 특징을 가지고 있음. Producer 와 Consumer 가 존재하고, 서로 의존적이지 않고 완벽하게 분리되어 있고, 브로커는 메시지를 한 번 저장하면 이후에는 수정할 수 없음
- 이러한 이유로 밑과 같은 문제 발생
  
  <img width="815" alt="Screenshot 2023-02-27 at 8 39 16 PM" src="https://user-images.githubusercontent.com/108987773/221554434-5450b649-ab4e-40c2-822e-21c380fae511.png">

  1. Producer 1과 2는 각자 브로커의 토픽 A 에 메시지를 보낸다.
  2. Consumer 는 토픽 A 에 있는 메시지를 읽는다.
  3. 이때, Producer 2가 schema 를 변경하여 메시지 (4번)를 발행한다.
  4. 하지만 Consumer 는 이 상황을 알지 못하기 때문에, 4번 메시지를 구독하여 처리하는 과정에서 메시지를 읽어드리지 못하고 장애가 발생한다.

- 이러한 문제에 더하여 동일한 schema 의 메시지가 계속 들어오는 경우, 같은 schema 를 계속해서 저장해야하기 때문에 메시지의 크기가 커지며, schema 가 중복이 되어 불필요한 데이터 용량을 차지하게 됨
- 이러한 구조적인 결합도를 낮추고 불필요한 데이터 용량을 줄이기 위해 Kafka 에서는 Schema Registry 를 사용. Schema Registry 란 메시지의 Schema 를 저장해주는 일종의 저장소
- Kafka Connector 가 만들어 내는 메시지 구조

  <img width="799" alt="Screenshot 2023-02-27 at 8 41 25 PM" src="https://user-images.githubusercontent.com/108987773/221554817-09890bfb-d1e1-4b05-866b-0cef13ac8477.png">
  
  - 메시지는 key 와 value 로 구성되어 있으며, 각 key 와 value 는 schema 와 payload 로 구성
  - 여기서 key 는 PK 와 같이 데이터를 식별할 수 있는 정보가 들어있고, value 는 데이터의 전체 값이 들어있음
  - payload 는 데이터 값이 저장되며, schema 에는 이 데이터 값의 데이터 타입이 명시
  
- Producer, Schema Registry, Kafka 간의 관계
  
  <img width="827" alt="Screenshot 2023-02-27 at 8 43 03 PM" src="https://user-images.githubusercontent.com/108987773/221555096-c91c540e-42d4-433c-b47f-5f4382843f58.png">
  
  - 과정
    - Producer 에서 Kafka 의 Serializer (또는 Converter) 에게 메시지를 보낸다.
    - Serializer 는 메시지를 받아 메시지의 schema 를 Schema Registry 에 보낸다.
    - 이어서 schema ID 를 받고, schema ID 와 데이터를 Kafka 에게 보낸다.
  
- 앞서 살펴봤던 schema 중복 문제는 Schema Registry 에 key 와 value 에 명시된 schema 를 따로 저장하기 때문에 Connector 가 schema 대신 Schema Registry 의 schema ID 를 명시하여 해결할 수 있게 됨
- Schema ID 를 쓰면 메세지의 크기가 줄어들어 불필요한 데이터의 용량도 줄일 수 있음
- 앞서 발생했던 내부적인 결합도 문제는 Schema Registry 에서 제공하는 기능 중 하나인 schema 호환성 규칙 강제 기능으로 해결할 수 있음. Schema 호환성 규칙 강제란 schema 를 등록하여 사용할 수 있지만, schema 버전 간의 호환성을 강제함으로써 일종의 규칙을 세우는 것

  <img width="807" alt="Screenshot 2023-02-27 at 8 45 56 PM" src="https://user-images.githubusercontent.com/108987773/221555633-70a1ec4c-1f47-4e44-9847-fcd34b6e1c73.png">
  
  - 여러 호환성 중 Forward 라는 호환성을 갖는 경우에 대한 예시
    1. Consumer 는 version 1로 메시지를 처리하고 있다.
    2. 그리고 Gender 라는 column 이 version 2에서 추가되었고, Consumer 는 version 2 의 schema 를 메시지를 구독하여 처리한다.
    3. 이때, Consumer 는 새로 추가된 column 을 제외하고, 기존 version 1에 맞춰 메시지를 처리한다.
    4. 이렇게 schema 의 호환성 규칙을 강제하여 schema 가 다른 메시지도 읽을 수 있도록 만든다.
---
# <4> Kafka System

<img width="328" alt="Screenshot 2023-02-27 at 8 47 47 PM" src="https://user-images.githubusercontent.com/108987773/221555974-29b1533b-5ed9-41b3-874c-bce16e812b16.png">

1. Kafka System
- [kafka-docker-compose.yaml][link1] : Zookeeper & Broker, Schema Registry
- [connect.Dockerfile][link2] : Connect을 생성하는 코드, 이미지를 build하기 위한 Dockerfile 필요
- 실행
  
  ```
  docker compose -p part7-kafka -f kafka-docker-compose.yaml up -d
  ```
  
  - 결과
    
    <img width="955" alt="Screenshot 2023-02-27 at 9 10 50 PM" src="https://user-images.githubusercontent.com/108987773/221560529-f99cc21f-3c84-4b4c-929b-4001d667d003.png">

  <img width="1355" alt="Screenshot 2023-02-27 at 9 11 17 PM" src="https://user-images.githubusercontent.com/108987773/221560618-400c04cf-2ef4-436a-b86a-d70c0d8a582b.png">

---
# <5> Source Connector

```
주의사항

01. Database 파트를 완료하고 DB 가 띄워진 상태에서 진행
```

1. Source Connect를 띄울 수 있는 [source_connector.json][link2] 작성

2. Source Connector 생성하는 json 파일을 curl 을 이용하여 Connect 의 REST API 에 POST method 로 보냄

  ```
  curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @source_connector.json
  ```
  
    - 결과
    
      <img width="1403" alt="Screenshot 2023-02-27 at 9 16 50 PM" src="https://user-images.githubusercontent.com/108987773/221561709-7fc7e83b-24e1-43cb-ae02-0753185c1014.png">

3. 생성 확인

  ```
  curl -X GET http://localhost:8083/connectors
  ```

    - 결과
    
      <img width="622" alt="Screenshot 2023-02-27 at 9 17 38 PM" src="https://user-images.githubusercontent.com/108987773/221561854-c688121a-4661-494d-a174-6883b1ff3329.png">

4. ```postgres-source-connector``` 정보 확인

  ```
  curl -X GET http://localhost:8083/connectors/postgres-source-connector
  ```
  
    - 결과
    
      <img width="1402" alt="Screenshot 2023-02-27 at 9 18 52 PM" src="https://user-images.githubusercontent.com/108987773/221562071-0fd723cd-ac06-49dc-9349-97b02b164274.png">
---
# <6> Sink Connector
1. Target Postgres Server
  - [create_table.py][link3] : Target DB 를 띄운 다음에 테이블만 생성하는 코드
  - [target.Dockerfile][link4] : 위에서 작성한 스크립트를 실행할 수 있는 이미지 만들기
  
2. 실행
  - [target-docker-compose.yaml][link5] : Docker Compose 를 이용하여 Target DB 서버와 Table Creator 를 띄우기
  - 터미널 명령어
    
    ```
    docker compose -p part7-target -f target-docker-compose.yaml up -d
    ```
    
    - 결과
      
      <img width="950" alt="Screenshot 2023-02-27 at 9 42 05 PM" src="https://user-images.githubusercontent.com/108987773/221566648-b5925f8d-4f4e-4939-9201-14dfeb134125.png">

3. Sink Connector
  - [sink_connector.json][link6] : Sink Connector 는 Source Connector 와 마찬가지로 Connect 에 API 호출을 통해 생성. 아래 명령어를 통해 Sink Connector 를 띄울 수 있는 sink_connector.json 을 생성
    - Sink Connector 생성하는 json 파일을 curl 을 이용하여 Connect 의 REST API 에 POST method 로 보내기
      
      ```
      curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @sink_connector.json
      ```
        - 결과
        
          <img width="877" alt="Screenshot 2023-02-27 at 9 42 48 PM" src="https://user-images.githubusercontent.com/108987773/221566800-222f55ac-47c8-4517-b817-945430bb9678.png">

4. 생성 확인
  - GET method 로 현재 Connector 목록을 확인 가능. 앞서 생성한 Connector 가 잘 있는지 확인
    
    ```
    curl -X GET http://localhost:8083/connectors
    ```
    
      - 결과
      
        <img width="623" alt="Screenshot 2023-02-27 at 9 43 36 PM" src="https://user-images.githubusercontent.com/108987773/221566943-f1ea10d7-4b76-45bd-a30c-03654a5b21e4.png">
  
  - ```postgres-sink-connector``` 의 정보를 확인
    
    ```
    curl -X GET http://localhost:8083/connectors/postgres-sink-connector
    ```
    
    - 결과
      
      <img width="876" alt="Screenshot 2023-02-27 at 9 44 19 PM" src="https://user-images.githubusercontent.com/108987773/221567071-c9b92f0a-02b8-48f3-8572-11b59da87ad2.png">

5. 데이터 확인

<img width="748" alt="Screenshot 2023-02-27 at 9 46 11 PM" src="https://user-images.githubusercontent.com/108987773/221567419-83a7ccea-fbb2-4bf2-b6e8-a87ed60ba3cf.png">

  
  

[link]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/07_Kafka/naive-docker-compose.yaml
[link1]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/07_Kafka/kafka-docker-compose.yaml/kafka-docker-compose.yaml
[link2]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/07_Kafka/source_connector.json
[link3]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/07_Kafka/create_table.py
[link4]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/07_Kafka/target.Dockerfile
[link5]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/07_Kafka/target-docker-compose.yaml
[link6]: https://github.com/jeewonkimm2/BOAZ_Big_Data_Study_Club/blob/main/StudyGroup/MLOps_for_MLE/07_Kafka/sink_connector.json
