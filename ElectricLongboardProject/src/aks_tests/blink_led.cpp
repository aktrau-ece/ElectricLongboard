#include "blink_led.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "components/led_strip/led_strip.h"
#include "sdkconfig.h"


#define LOG_TAG "AKS_TESTS"
#define LOG_LEVEL_LOCAL ESP_LOG_VERBOSE

#define LED_PIN GPIO_NUM_8

#define pdSECOND pdMS_TO_TICKS(1000)

static led_strip_handle_t led_strip;

extern "C" {

    void blinkLed() {
        
    	esp_rom_gpio_pad_select_gpio(LED_PIN);
    	gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);

        while(true) {

            ESP_LOGI(LOG_TAG, "LED on");
            vTaskDelay(pdSECOND * 2);
            led_strip_set_pixel(led_strip, 0, 16, 16, 16);
            led_strip_refresh(led_strip);

            ESP_LOGI(LOG_TAG, "LED off");
            vTaskDelay(pdSECOND * 2);
            gpio_set_level(LED_PIN, 0);
            led_strip_clear(led_strip);
       	}
    }
}