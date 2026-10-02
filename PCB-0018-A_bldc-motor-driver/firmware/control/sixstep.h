/* sixstep.h - sensored six-step commutation from three hall sensors.
 *
 * Hall code h = HA | HB<<1 | HC<<2. With 120-degree sensors, forward rotation
 * visits 1,3,2,6,4,5 and 0/7 never occur (a broken wire or sensor).
 * Step k (0..5) drives: 0 A+B-, 1 A+C-, 2 B+C-, 3 B+A-, 4 C+A-, 5 C+B-.
 * Which hall code lines up with which step depends on the motor and on how
 * the sensors are mounted: tune the table on hardware (the motor stage). */
#ifndef SIXSTEP_H
#define SIXSTEP_H

#include <stdint.h>

/* Per phase: +1 = high side PWM, -1 = low side on, 0 = floating. */
typedef struct { int8_t a, b, c; } sixstep_drive_t;

/* Step 0..5 for a hall code, or -1 for an invalid code (0 or 7 or >7). */
int sixstep_step(uint8_t hall);
/* Drive pattern for a hall code; reverse != 0 swaps the signs.
 * Returns 0, or -1 for an invalid code (the caller latches FAULT_HALL and
 * *out is all-floating). */
int sixstep_drive(uint8_t hall, int reverse, sixstep_drive_t *out);

/* Pack three sensor levels (any nonzero = high) into a hall code. */
uint8_t sixstep_hall_code(int ha, int hb, int hc);

/* Turn a drive pattern into per-phase TIM1 settings:
 *   +1 -> d = duty, low side enabled (complementary, synchronous PWM)
 *   -1 -> d = 0,    low side enabled (low side on the whole period)
 *    0 -> d = 0,    low side disabled (both gates held low: floating)
 * duty is clamped to 0..1 (NaN -> 0). */
void sixstep_phase_out(const sixstep_drive_t *drv, float duty, float d[3], uint8_t lo_en[3]);

/* Open-loop duty with a soft current limit: the commanded duty, capped at
 * max_duty, or 0 while the largest phase current is at or over i_soft_a
 * (a NaN current also gives 0). */
float sixstep_limit_duty(float cmd, float max_duty, float i_peak_a, float i_soft_a);

#endif
