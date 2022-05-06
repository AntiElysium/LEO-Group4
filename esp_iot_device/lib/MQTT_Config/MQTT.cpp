#include <PubSubClient.h>
#include <WiFi.h>
#include <MQTT.h>

WiFiClient wifi_client;
PubSubClient client(wifi_client);

struct Subscription {
    const char* topic;
    SubscriptionCallback callback;
    struct Subscription* next;
};

const char* broker_address = "broker.mqttdashboard.com";
const char* DEVICE_ID = "aksdfngkjasndg";

Subscription* head = NULL;

void printMessage(char* topic, byte* message, unsigned int length) {
    Serial.print("Topic: ");
    Serial.println(topic);

    Serial.print("Message: ");
    String messageTemp;
    for (int i = 0; i < length; i++) {
        Serial.print((char)message[i]);
        messageTemp += (char)message[i];
    }
    Serial.println();
}

void callback(char* topic, byte* message, unsigned int length) {
    printMessage(topic, message, length);

    struct Subscription* temp = head;
    while (temp != NULL) {
        if (String(temp->topic) == String(topic)) {
            temp->callback(message, length);
        }

        temp = temp->next;
    }


}

void subscribeToTopic(const char* topic, SubscriptionCallback callback) {
    client.subscribe(topic);

    if (head == NULL) {
        head = (Subscription*) malloc (sizeof(Subscription));
        head->topic = topic;
        head->callback = callback;
        head->next = NULL;
    } else {
        struct Subscription* temp = head;
        while (temp->next != NULL) {
            temp = temp->next;
        }
        temp->next = (Subscription*) malloc (sizeof(Subscription));
        temp->next->topic = topic;
        temp->next->callback = callback;
        temp->next->next = NULL;
    }
}

void publishToTopic(const char* topic, const char* message) {
    client.publish(topic, message);
}

void loopMQTT() {
    client.loop();
}

void initMQTT() {
    client.setServer(broker_address, 1883);
    client.setCallback(callback);

    while (!client.connected()) {
        if (client.connect(DEVICE_ID)) {
            Serial.println("Connected to MQTT");
        } else {
            Serial.println("Failed to connect, trying again in 5 seconds");
            delay(5000);
        }
    }
    Serial.println("Connection done");
}

