#include "IbraKernel.h"

#include <SPI.h>
#include <Arduino.h>
#include <vector>
#include "Adafruit_GFX.h"
#include "System/Mjolnir.h"

void KernelBootAnimation(void);

void setup(void) {
  IbraKernel::IO IOWork;
  if (!IOWork.Init()) {
    return;
  }
  KernelBootAnimation();
}

void KernelBootAnimation() {
  IbraKernel::IO::Display->GetTFT()->setRotation(1);
  IbraKernel::IO::Display->GetTFT()->fillScreen(HX8357_WHITE);

  // Draw IbraOS logo.
  IbraKernel::IO::Display->GetTFT()->setCursor(150, 150);
  IbraKernel::IO::Display->GetTFT()->setTextColor(HX8357_BLACK);
  IbraKernel::IO::Display->GetTFT()->setTextSize(5);
  IbraKernel::IO::Display->GetTFT()->println("IbraOS");

  delay(3000);

  IbraKernel::IO::Display->GetTFT()->setCursor(0, 0);
  IbraKernel::IO::Display->GetTFT()->fillScreen(HX8357_BLACK);

  // Run main menu.
  IbraKernel::REX Interp;
  Interp.RunFromFile("boot.rex");
}

void loop() {}