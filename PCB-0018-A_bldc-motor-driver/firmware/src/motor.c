/* motor.c - stage 2: sensored six-step from the Halls, open-loop duty.
 *
 * The hall inputs (HALL_A/B/C, RC-filtered on the board, so no internal pull)
 * interrupt on both edges; each edge re-reads the three levels and applies
 * the step at once. The main loop re-applies it on every pass too, which
 * catches a missed edge and brings in the soft current limit.
 *
 * Safety (design.md): six-step only runs while armed with no fault latched;
 * a fault or `disarm` clears g_app.six_on in pwm_disarm() and drops MOE, so
 * the bridge coasts. An invalid hall code (0 or 7) floats all three phases at
 * once and latches FAULT_HALL. Duty is open loop, capped at SIXSTEP_MAX_DUTY
 * and cut to 0 while any phase is at or over SIXSTEP_I_SOFT_A; I_LIMIT_A
 * (software latch) and I_TRIP_A (hardware break) stay above that.
 *
 * NOT verified: the hall-to-step table (control/sixstep.c) against a real
 * motor, and commutation timing: CCR writes are preloaded (next update) but
 * CCxNE changes at once, so for up to one PWM period after an edge the bridge
 * can still drive the previous step. No phase is ever driven high and low
 * together: the timer's dead time covers each complementary pair. */
#include "app.h"
#include "sixstep.h"

typedef struct { GPIO_TypeDef *port; uint32_t pin; } hall_pin_t;

static const hall_pin_t k_hall[3] = {
    { PIN_HALL_A_PORT, PIN_HALL_A_PIN },
    { PIN_HALL_B_PORT, PIN_HALL_B_PIN },
    { PIN_HALL_C_PORT, PIN_HALL_C_PIN },
};

static uint32_t s_exti_mask;
static volatile float s_duty_cmd, s_duty_now;
static volatile int s_reverse;
static volatile uint32_t s_edges;
static volatile int s_bad; /* an edge saw an invalid code while running */

uint8_t motor_hall_read(void)
{
    return sixstep_hall_code(gpio_read(k_hall[0].port, k_hall[0].pin),
                             gpio_read(k_hall[1].port, k_hall[1].pin),
                             gpio_read(k_hall[2].port, k_hall[2].pin));
}

uint32_t motor_edges(void)
{
    return s_edges;
}

static IRQn_Type exti_irq(uint32_t line)
{
    switch (line) {
    case 0u: return EXTI0_IRQn;
    case 1u: return EXTI1_IRQn;
    case 2u: return EXTI2_IRQn;
    case 3u: return EXTI3_IRQn;
    case 4u: return EXTI4_IRQn;
    default: return line <= 9u ? EXTI9_5_IRQn : EXTI15_10_IRQn;
    }
}

void motor_init(void)
{
    RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;
    (void)RCC->APB2ENR;
    for (int k = 0; k < 3; k++) {
        GPIO_TypeDef *g = k_hall[k].port;
        uint32_t n = k_hall[k].pin;
        uint32_t port = ((uint32_t)g - GPIOA_BASE) / (GPIOB_BASE - GPIOA_BASE);
        g->PUPDR &= ~(3u << (n * 2u));                 /* the board filters and pulls */
        gpio_mode(g, n, GPIO_IN);                      /* PA15/PB3 leave JTAG; SWD stays */
        SYSCFG->EXTICR[n / 4u] = (SYSCFG->EXTICR[n / 4u] & ~(0xFu << ((n % 4u) * 4u)))
                               | (port << ((n % 4u) * 4u));
        s_exti_mask |= 1u << n;
    }
    EXTI->RTSR1 |= s_exti_mask;
    EXTI->FTSR1 |= s_exti_mask;
    EXTI->PR1 = s_exti_mask;
    EXTI->IMR1 |= s_exti_mask;
    for (int k = 0; k < 3; k++) {
        IRQn_Type irq = exti_irq(k_hall[k].pin);
        NVIC_SetPriority(irq, 1u); /* above the console (2) */
        NVIC_EnableIRQ(irq);
    }
    g_app.hall = motor_hall_read();
}

/* Apply the step for the current hall code. Called from the EXTI handler and,
 * with interrupts off, from the main loop. */
static void apply(void)
{
    if (!g_app.six_on || !g_app.armed) return;
    uint8_t h = motor_hall_read();
    sixstep_drive_t drv;
    float d[3];
    uint8_t lo[3];
    if (sixstep_drive(h, s_reverse, &drv)) s_bad = 1; /* drv floats every phase */
    sixstep_phase_out(&drv, s_duty_now, d, lo);
    pwm_set_phase(d, lo);
    g_app.hall = h;
}

static void hall_isr(void)
{
    uint32_t pr = EXTI->PR1 & s_exti_mask;
    if (!pr) return;
    EXTI->PR1 = pr;
    s_edges++;
    apply();
}

void EXTI0_IRQHandler(void) { hall_isr(); }
void EXTI1_IRQHandler(void) { hall_isr(); }
void EXTI2_IRQHandler(void) { hall_isr(); }
void EXTI3_IRQHandler(void) { hall_isr(); }
void EXTI4_IRQHandler(void) { hall_isr(); }
void EXTI9_5_IRQHandler(void) { hall_isr(); }
void EXTI15_10_IRQHandler(void) { hall_isr(); }

int motor_start(float duty, int reverse)
{
    if (sixstep_step(motor_hall_read()) < 0) return -1;
    uint32_t pm = __get_PRIMASK();
    __disable_irq();
    s_reverse = reverse;
    s_duty_cmd = duty;
    if (!g_app.six_on) {
        s_duty_now = 0.0f; /* the next main-loop pass applies the limited duty */
        s_bad = 0;
        g_app.six_on = 1;
        apply();
    }
    __set_PRIMASK(pm);
    return 0;
}

int motor_reverse(void)
{
    return s_reverse;
}

uint32_t motor_hall_fault(void)
{
    if (!g_app.six_on) { s_bad = 0; return 0u; }
    int bad = s_bad || sixstep_step(motor_hall_read()) < 0;
    s_bad = 0;
    return bad ? FAULT_HALL : 0u;
}

void motor_poll(void)
{
    if (!g_app.six_on) {
        g_app.hall = motor_hall_read();
        return;
    }
    float ipk = 0.0f;
    for (int k = 0; k < 3; k++) {
        float a = g_app.i_a[k] < 0.0f ? -g_app.i_a[k] : g_app.i_a[k];
        if (!(a <= ipk)) ipk = a; /* NaN propagates, and the limiter reads it as over */
    }
    uint32_t pm = __get_PRIMASK();
    __disable_irq();
    s_duty_now = sixstep_limit_duty(s_duty_cmd, SIXSTEP_MAX_DUTY, ipk, SIXSTEP_I_SOFT_A);
    apply();
    __set_PRIMASK(pm);
}
