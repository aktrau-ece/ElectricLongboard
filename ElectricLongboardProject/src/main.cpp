#include "main.h"
#include "esp_log.h"
#include "driver/gpio.h"

#include "aks_tests/aks_tests.h"


#define LOG_TAG "MAIN"
#define LOG_LEVEL_LOCAL ESP_LOG_VERBOSE


extern "C" {
    void app_main() {
        
        blinkLed();
    }
}