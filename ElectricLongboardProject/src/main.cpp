#include "esp_log.h"

extern "C" {
    void app_main() {
        static const char* TAG = "MAIN";
        ESP_LOGD(TAG, "Hello world from the master branch");
    }
}