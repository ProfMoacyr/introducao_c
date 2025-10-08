#include "driver/gpio.h"
#include <string.h> // Para memset
#include "freertos/FreeRTOS.h"

void configurar_gpio_seguro(gpio_num_t pino)
{
	gpio_config_t cfg;

	// 1. Zerar a struct para garantir que todos os campos sejam 0
	memset(&cfg, 0, sizeof(gpio_config_t));

	// 2. Configurar APENAS os campos necessários
	cfg.pin_bit_mask = (1ULL << pino);
	cfg.mode = GPIO_MODE_OUTPUT;

	// 3. Aplicar a configuracao (passando o ENDEREÇO da struct)
	gpio_config(&cfg);
}

void app_main()
{
	// Configura GPIO 2 de forma segura
	configurar_gpio_seguro(GPIO_NUM_2);

	// Loop de blink simples
	while (1)
	{
		gpio_set_level(GPIO_NUM_2, 1);
		vTaskDelay(1000 / portTICK_PERIOD_MS);
		gpio_set_level(GPIO_NUM_2, 0);
		vTaskDelay(1000 / portTICK_PERIOD_MS);
	}
}
