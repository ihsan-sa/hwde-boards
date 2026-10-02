#include "sixstep.h"

static const int8_t hall_to_step[8] = { -1, 0, 2, 1, 4, 5, 3, -1 };

static const sixstep_drive_t step_drive[6] = {
    { +1, -1, 0 }, { +1, 0, -1 }, { 0, +1, -1 },
    { -1, +1, 0 }, { -1, 0, +1 }, { 0, -1, +1 },
};

int sixstep_step(uint8_t hall)
{
    return hall < 8u ? hall_to_step[hall] : -1;
}

int sixstep_drive(uint8_t hall, int reverse, sixstep_drive_t *out)
{
    int k = sixstep_step(hall);
    if (k < 0) {
        out->a = out->b = out->c = 0;
        return -1;
    }
    *out = step_drive[k];
    if (reverse) {
        out->a = (int8_t)-out->a;
        out->b = (int8_t)-out->b;
        out->c = (int8_t)-out->c;
    }
    return 0;
}

uint8_t sixstep_hall_code(int ha, int hb, int hc)
{
    return (uint8_t)((ha ? 1u : 0u) | (hb ? 2u : 0u) | (hc ? 4u : 0u));
}

static float clamp01(float v)
{
    if (!(v > 0.0f)) return 0.0f; /* also NaN */
    return v > 1.0f ? 1.0f : v;
}

void sixstep_phase_out(const sixstep_drive_t *drv, float duty, float d[3], uint8_t lo_en[3])
{
    const int8_t p[3] = { drv->a, drv->b, drv->c };
    duty = clamp01(duty);
    for (int k = 0; k < 3; k++) {
        d[k] = p[k] > 0 ? duty : 0.0f;
        lo_en[k] = p[k] != 0 ? 1u : 0u;
    }
}

float sixstep_limit_duty(float cmd, float max_duty, float i_peak_a, float i_soft_a)
{
    if (!(i_peak_a < i_soft_a)) return 0.0f;
    cmd = clamp01(cmd);
    return cmd > max_duty ? clamp01(max_duty) : cmd;
}
