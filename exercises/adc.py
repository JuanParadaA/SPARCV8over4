from uctypes import BF_POS, BF_LEN, UINT32, BFUINT32, struct

# Base addresses for GPIO and ADC peripherals (RP2040 chip)
GPIO_BASE = 0x40014000       # Base address for GPIO registers
GPIO_CHAN_WIDTH = 0x08       # Offset for each GPIO channel
GPIO_PIN_COUNT = 30          # Number of GPIO pins available
ADC_BASE = 0x4004c000        # Base address for ADC registers

# Define bitfield layouts for GPIO status and control registers 
GPIO_STATUS_FIELDS = {
    "IRQTOPROC":  26<<BF_POS | 1<<BF_LEN | BFUINT32,  # IRQ to processor flag
    "IRQFROMPAD": 24<<BF_POS | 1<<BF_LEN | BFUINT32,  # IRQ from GPIO pad flag
    "INTOPERI":   19<<BF_POS | 1<<BF_LEN | BFUINT32,  # Interrupt to peripheral flag
    "INFROMPAD":  17<<BF_POS | 1<<BF_LEN | BFUINT32,  # Input from pad status
    "OETOPAD":    13<<BF_POS | 1<<BF_LEN | BFUINT32,  # Output enable to pad status
    "OEFROMPERI": 12<<BF_POS | 1<<BF_LEN | BFUINT32,  # Output enable from peripheral status
    "OUTTOPAD":    9<<BF_POS | 1<<BF_LEN | BFUINT32,  # Output to pad status
    "OUTFROMPERI": 8<<BF_POS | 1<<BF_LEN | BFUINT32   # Output from peripheral status
}

# Define bitfield layouts for GPIO control registers
GPIO_CTRL_FIELDS = {
    "IRQOVER":    28<<BF_POS | 2<<BF_LEN | BFUINT32,  # IRQ override control
    "INOVER":     16<<BF_POS | 2<<BF_LEN | BFUINT32,  # Input override control
    "OEOVER":     12<<BF_POS | 2<<BF_LEN | BFUINT32,  # Output enable override control
    "OUTOVER":     8<<BF_POS | 2<<BF_LEN | BFUINT32,  # Output override control
    "FUNCSEL":     0<<BF_POS | 5<<BF_LEN | BFUINT32   # Pin function selection
}

# Register map for GPIO peripheral
GPIO_REGS = {
    "GPIO_STATUS_REG": 0x00|UINT32,                  # Status register address
    "GPIO_STATUS":     (0x00, GPIO_STATUS_FIELDS),   # Status register fields
    "GPIO_CTRL_REG":   0x04|UINT32,                  # Control register address
    "GPIO_CTRL":       (0x04, GPIO_CTRL_FIELDS)      # Control register fields
}

# Define bitfield layouts for ADC control and status registers 
ADC_CS_FIELDS = {
    "RROBIN":     16<<BF_POS | 5<<BF_LEN | BFUINT32,  # Round-robin channel select
    "AINSEL":     12<<BF_POS | 3<<BF_LEN | BFUINT32,  # Analog input select
    "ERR_STICKY": 10<<BF_POS | 1<<BF_LEN | BFUINT32,  # Sticky error flag
    "ERR":         9<<BF_POS | 1<<BF_LEN | BFUINT32,  # Error flag
    "READY":       8<<BF_POS | 1<<BF_LEN | BFUINT32,  # ADC ready flag
    "START_MANY":  3<<BF_POS | 1<<BF_LEN | BFUINT32,  # Start many conversions
    "START_ONCE":  2<<BF_POS | 1<<BF_LEN | BFUINT32,  # Start a single conversion
    "TS_EN":       1<<BF_POS | 1<<BF_LEN | BFUINT32,  # Temperature sensor enable
    "EN":          0<<BF_POS | 1<<BF_LEN | BFUINT32   # ADC enable flag
}

# Define bitfield layouts for ADC FIFO control and status registers
ADC_FCS_FIELDS = {
    "THRESH":     24<<BF_POS | 4<<BF_LEN | BFUINT32,  # FIFO threshold level
    "LEVEL":      16<<BF_POS | 4<<BF_LEN | BFUINT32,  # FIFO level
    "OVER":       11<<BF_POS | 1<<BF_LEN | BFUINT32,  # FIFO overflow flag
    "UNDER":      10<<BF_POS | 1<<BF_LEN | BFUINT32,  # FIFO underflow flag
    "FULL":        9<<BF_POS | 1<<BF_LEN | BFUINT32,  # FIFO full flag
    "EMPTY":       8<<BF_POS | 1<<BF_LEN | BFUINT32,  # FIFO empty flag
    "DREQ_EN":     3<<BF_POS | 1<<BF_LEN | BFUINT32,  # DMA request enable
    "ERR":         2<<BF_POS | 1<<BF_LEN | BFUINT32,  # FIFO error flag
    "SHIFT":       1<<BF_POS | 1<<BF_LEN | BFUINT32,  # Data shift flag
    "EN":          0<<BF_POS | 1<<BF_LEN | BFUINT32   # FIFO enable flag
}

# Register map for ADC peripheral
ADC_REGS = {
    "CS_REG":     0x00|UINT32,                # Control and status register
    "CS":         (0x00, ADC_CS_FIELDS),      # Control and status fields
    "RESULT_REG": 0x04|UINT32,                # Conversion result register
    "FCS_REG":    0x08|UINT32,                # FIFO control and status register
    "FCS":        (0x08, ADC_FCS_FIELDS),     # FIFO control and status fields
    "FIFO_REG":   0x0c|UINT32,                # FIFO register
    "DIV_REG":    0x10|UINT32,                # Clock divisor register
    "INTR_REG":   0x14|UINT32,                # Interrupt raw register
    "INTE_REG":   0x18|UINT32,                # Interrupt enable register
    "INTF_REG":   0x1c|UINT32,                # Interrupt force register
    "INTS_REG":   0x20|UINT32                 # Interrupt status register
}

# Initialize GPIO pins as structs to access their control and status registers
GPIO_PINS = [struct(GPIO_BASE + n*GPIO_CHAN_WIDTH, GPIO_REGS) for n in range(0, GPIO_PIN_COUNT)]
ADC_DEVICE = struct(ADC_BASE, ADC_REGS)  # Initialize ADC device as a struct

# Define a GPIO function constant to reset a pin's function
GPIO_FUNC_NULL = 0x1f  # Null function (disable pin)

import array, time, uctypes, math, random

# Constants for ADC configuration
ADC_CHAN = 0                # ADC channel to use (channel 0)
ADC_PIN = 26 + ADC_CHAN      # Corresponding GPIO pin for the ADC channel
ADC_SAMPLES = 20             # Number of ADC samples to read
MIN_SAMPLES, MAX_SAMPLES = 10, 1000  # Range for ADC sample size
ADC_RATE = 100000            # ADC sample rate (in Hz)
MIN_RATE, MAX_RATE = 1000, 500000  # Range for ADC sample rate

adc = ADC_DEVICE  # Alias for the initialized ADC device struct

# Initialize the ADC and configure the GPIO pin for ADC use
def adc_init():
    pin = GPIO_PINS[ADC_PIN]          # Select the GPIO pin for the ADC channel
    pin.GPIO_CTRL_REG = GPIO_FUNC_NULL  # Configure the pin as an ADC input (set function to null)
    adc.CS_REG = 0  # Reset ADC control register
    adc.CS.EN = 1   # Enable the ADC
    adc.CS.AINSEL = ADC_CHAN  # Select the ADC channel to read from

# Perform a single ADC conversion and return the result in voltage
def adc_read():
    adc.CS.START_ONCE = 1  # Start a single ADC conversion
    while not adc.CS.READY:  # Wait until the conversion is ready
        pass
    result = adc.RESULT_REG  # Read the ADC result register
    return result * 3.3 / 4096  # Convert the result to a voltage (3.3V reference, 12-bit ADC)

# Initialize the ADC and repeatedly read values with a 1-second delay
import time
adc_init()  # Initialize the ADC
for i in range(100):  # Perform 100 ADC readings
    print(adc_read())  # Print the ADC value converted to voltage
    time.sleep(1)      # Wait for 1 second between readings

