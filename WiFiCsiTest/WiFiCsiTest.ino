#include <Arduino.h>
#include <WiFi.h>
#include "wifi_conf.h"
#include "wifi_ind.h"
#include "wifi_secrets.h"

char ssid[] = TEST_WIFI_SSID;
char password[] = TEST_WIFI_PASSWORD;
static uint8_t raw[16384];
static volatile unsigned int events = 0;
static unsigned int handled = 0;
static unsigned long validReports = 0;
static bool csiEnabled = false;

void csiDone(char *, int, int, void *) { ++events; }

void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.println("WIFI_CSI_TEST v1");
  for (int attempt = 0; attempt < 3 && WiFi.status() != WL_CONNECTED; ++attempt) {
    Serial.print("WIFI_CONNECT attempt="); Serial.println(attempt + 1);
    WiFi.begin(ssid, password);
    delay(3000);
  }
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WIFI_CONNECT_FAILED");
    return;
  }
  Serial.print("WIFI_CONNECTED ip="); Serial.println(WiFi.localIP());
  Serial.print("RSSI="); Serial.println(WiFi.RSSI());
  wifi_reg_event_handler(WIFI_EVENT_CSI_DONE, csiDone, NULL);
  // Initial probe settings, not a validated capture profile.
  rtw_csi_action_parm_t cfg = {};
  cfg.act = CSI_ACT_CFG;
  cfg.mode = CSI_MODE_NORMAL;
  cfg.group_num = CSI_GROUP_NUM_1;
  cfg.accuracy = CSI_ACCU_1BYTE;
  cfg.trig_period = 100;
  cfg.data_rate = MGN_MCS0;
  int rc = wifi_csi_config(&cfg);
  Serial.print("CSI_CONFIG rc="); Serial.println(rc);
  if (rc != RTW_SUCCESS) return;
  cfg.act = CSI_ACT_EN;
  cfg.enable = 1;
  rc = wifi_csi_config(&cfg);
  Serial.print("CSI_ENABLE rc="); Serial.println(rc);
  csiEnabled = (rc == RTW_SUCCESS);
  Serial.println("Generate traffic by pinging the board IP.");
}

void loop() {
  static unsigned long lastStatus = 0;
  if (csiEnabled && events != handled) {
    handled = events;
    rtw_csi_header_t header = {};
    u32 length = 0;
    int rc = wifi_csi_report(sizeof(raw), raw, &length, &header);
    Serial.print("CSI_REPORT rc="); Serial.print(rc);
    Serial.print(" valid="); Serial.print(header.csi_valid);
    Serial.print(" bytes="); Serial.print(length);
    Serial.print(" tones="); Serial.print(header.num_sub_carrier);
    Serial.print(" timestamp="); Serial.println(header.hw_assigned_timestamp);
    if (rc == RTW_SUCCESS && header.csi_valid && length > 0 && length <= sizeof(raw)) {
      ++validReports;
      Serial.print("CSI_PREVIEW_HEX=");
      for (u32 i = 0; i < length && i < 32; ++i) {
        if (raw[i] < 16) Serial.print('0');
        Serial.print(raw[i], HEX);
      }
      Serial.println();
    }
  }
  if (millis() - lastStatus >= 5000) {
    lastStatus = millis();
    Serial.print("STATUS wifi="); Serial.print(WiFi.status());
    Serial.print(" ip="); Serial.print(WiFi.localIP());
    Serial.print(" csi_enabled="); Serial.print(csiEnabled);
    Serial.print(" events="); Serial.print(events);
    Serial.print(" valid_reports="); Serial.println(validReports);
  }
  delay(10);
}
