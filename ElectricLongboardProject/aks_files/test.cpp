#include "esp_log.h"
// #include "driver/gpio.h"

extern "C" {
    void app_main() {
        esp_log_level_set("*", ESP_LOG_DEBUG);
        static const char* TAG = "MAIN";
        ESP_LOGD(TAG, "Hello world A");

        // gpio_set_direction(GPIO_NUM_2, GPIO_MODE_OUTPUT);

        // while(true) {
        //     gpio_set_level(GPIO_NUM_2, 1);
        // }
    }
}