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
