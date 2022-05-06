#if !defined(MQTT_Config)
#define MQTT_Config
    #include <Arduino.h>
    typedef void (*SubscriptionCallback) (byte* message, unsigned int length);
    void initMQTT();
    void subscribeToTopic(const char*, SubscriptionCallback);
    void publishToTopic(const char* topic, const char* message);
    void loopMQTT();
    void printMessage(char* topic, byte* message, unsigned int length);
#endif