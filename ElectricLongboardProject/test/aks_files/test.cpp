#include "esp_log.h"

extern "C" {
    void app_main() {
        esp_log_level_set("*", ESP_LOG_DEBUG);
        static const char* TAG = "MAIN";
        ESP_LOGD(TAG, "Hello world");

    }
}