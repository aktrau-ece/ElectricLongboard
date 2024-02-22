#include "hello_world.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"


#define pdSECOND pdMS_TO_TICKS(1000)

#define LOG_TAG "AKS_TESTS"
#define LOG_LEVEL_LOCAL ESP_LOG_VERBOSE


extern "C" {

    void helloWorld() {
        
        while(true) {
            ESP_LOGI(LOG_TAG, "Hello world!!");
            vTaskDelay(pdSECOND * 2);
        }
    }
}