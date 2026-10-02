#include "check.h"
#include "sixstep.h"

int main(void)
{
    const uint8_t fwd[6] = { 1, 3, 2, 6, 4, 5 };
    sixstep_drive_t d;

    /* every valid code drives exactly one high and one low phase */
    for (uint8_t h = 1; h <= 6; h++) {
        CHECK_EQ(sixstep_drive(h, 0, &d), 0);
        CHECK_EQ((d.a == 1) + (d.b == 1) + (d.c == 1), 1);
        CHECK_EQ((d.a == -1) + (d.b == -1) + (d.c == -1), 1);
        CHECK_EQ(d.a + d.b + d.c, 0);
    }
    /* forward hall sequence walks the steps 0..5 in order */
    for (int k = 0; k < 6; k++) CHECK_EQ(sixstep_step(fwd[k]), k);
    /* known steps */
    sixstep_drive(1, 0, &d);
    CHECK(d.a == 1 && d.b == -1 && d.c == 0);
    sixstep_drive(5, 0, &d);
    CHECK(d.a == 0 && d.b == -1 && d.c == 1);
    /* reverse swaps high and low */
    sixstep_drive(1, 1, &d);
    CHECK(d.a == -1 && d.b == 1 && d.c == 0);

    /* invalid codes: 0 and 7 (and anything wider) are faults, bridge floats */
    CHECK_EQ(sixstep_step(0), -1);
    CHECK_EQ(sixstep_step(7), -1);
    CHECK_EQ(sixstep_step(200), -1);
    d.a = 1;
    CHECK_EQ(sixstep_drive(0, 0, &d), -1);
    CHECK(d.a == 0 && d.b == 0 && d.c == 0);
    CHECK_EQ(sixstep_drive(7, 1, &d), -1);

    /* the full commutation table, forward: step k drives the pair in sixstep.h */
    static const sixstep_drive_t want[6] = {
        { +1, -1, 0 }, { +1, 0, -1 }, { 0, +1, -1 },
        { -1, +1, 0 }, { -1, 0, +1 }, { 0, -1, +1 },
    };
    for (int k = 0; k < 6; k++) {
        CHECK_EQ(sixstep_drive(fwd[k], 0, &d), 0);
        CHECK(d.a == want[k].a && d.b == want[k].b && d.c == want[k].c);
        /* reverse is the same pair with high and low swapped */
        CHECK_EQ(sixstep_drive(fwd[k], 1, &d), 0);
        CHECK(d.a == -want[k].a && d.b == -want[k].b && d.c == -want[k].c);
    }
    /* consecutive forward steps differ in exactly one phase (one switch per edge) */
    for (int k = 0; k < 6; k++) {
        const sixstep_drive_t *x = &want[k], *y = &want[(k + 1) % 6];
        CHECK_EQ((x->a != y->a) + (x->b != y->b) + (x->c != y->c), 2);
        CHECK_EQ((x->a == y->a && x->a != 0) + (x->b == y->b && x->b != 0)
                 + (x->c == y->c && x->c != 0), 1);
    }
    /* every hall code 0..7 maps to a distinct step or to invalid */
    int seen[6] = { 0 };
    for (uint8_t h = 0; h < 8; h++) {
        int k = sixstep_step(h);
        if (h == 0 || h == 7) { CHECK_EQ(k, -1); continue; }
        CHECK(k >= 0 && k < 6);
        if (k >= 0 && k < 6) seen[k]++;
    }
    for (int k = 0; k < 6; k++) CHECK_EQ(seen[k], 1);

    /* hall decoding: HA is bit 0, HB bit 1, HC bit 2; any nonzero is high */
    CHECK_EQ(sixstep_hall_code(0, 0, 0), 0);
    CHECK_EQ(sixstep_hall_code(1, 0, 0), 1);
    CHECK_EQ(sixstep_hall_code(0, 1, 0), 2);
    CHECK_EQ(sixstep_hall_code(0, 0, 1), 4);
    CHECK_EQ(sixstep_hall_code(1, 1, 0), 3);
    CHECK_EQ(sixstep_hall_code(0, 1, 1), 6);
    CHECK_EQ(sixstep_hall_code(1, 0, 1), 5);
    CHECK_EQ(sixstep_hall_code(1, 1, 1), 7);
    CHECK_EQ(sixstep_hall_code(1 << 15, 8, 1 << 10), 7); /* raw IDR bits, not 0/1 */
    for (int m = 0; m < 8; m++)
        CHECK_EQ(sixstep_hall_code(m & 1, m & 2, m & 4), m);

    /* phase outputs: +1 PWMs at duty with its low side, -1 holds the low side on,
     * 0 floats (duty 0 and low side off) */
    float dd[3];
    uint8_t lo[3];
    sixstep_drive(1, 0, &d); /* A+ B- C float */
    sixstep_phase_out(&d, 0.3f, dd, lo);
    CHECK_NEAR(dd[0], 0.3, 1e-6); CHECK_NEAR(dd[1], 0.0, 1e-6); CHECK_NEAR(dd[2], 0.0, 1e-6);
    CHECK(lo[0] == 1 && lo[1] == 1 && lo[2] == 0);
    sixstep_drive(5, 1, &d); /* reverse of C+ B-: C- B+ A float */
    sixstep_phase_out(&d, 0.5f, dd, lo);
    CHECK_NEAR(dd[0], 0.0, 1e-6); CHECK_NEAR(dd[1], 0.5, 1e-6); CHECK_NEAR(dd[2], 0.0, 1e-6);
    CHECK(lo[0] == 0 && lo[1] == 1 && lo[2] == 1);
    sixstep_drive(0, 0, &d); /* invalid: everything floats */
    sixstep_phase_out(&d, 0.5f, dd, lo);
    CHECK(dd[0] == 0.0f && dd[1] == 0.0f && dd[2] == 0.0f);
    CHECK(lo[0] == 0 && lo[1] == 0 && lo[2] == 0);
    sixstep_drive(1, 0, &d);
    sixstep_phase_out(&d, 2.0f, dd, lo);  CHECK_NEAR(dd[0], 1.0, 1e-6);
    sixstep_phase_out(&d, -1.0f, dd, lo); CHECK_NEAR(dd[0], 0.0, 1e-6);
    sixstep_phase_out(&d, NAN, dd, lo);   CHECK_NEAR(dd[0], 0.0, 1e-6);

    /* soft current limit and duty cap */
    CHECK_NEAR(sixstep_limit_duty(0.2f, 0.5f, 3.0f, 10.0f), 0.2, 1e-6);
    CHECK_NEAR(sixstep_limit_duty(0.8f, 0.5f, 3.0f, 10.0f), 0.5, 1e-6);
    CHECK_NEAR(sixstep_limit_duty(0.2f, 0.5f, 10.0f, 10.0f), 0.0, 1e-6); /* at the limit */
    CHECK_NEAR(sixstep_limit_duty(0.2f, 0.5f, 9.99f, 10.0f), 0.2, 1e-6);
    CHECK_NEAR(sixstep_limit_duty(0.2f, 0.5f, NAN, 10.0f), 0.0, 1e-6);
    CHECK_NEAR(sixstep_limit_duty(NAN, 0.5f, 1.0f, 10.0f), 0.0, 1e-6);
    CHECK_NEAR(sixstep_limit_duty(-0.3f, 0.5f, 1.0f, 10.0f), 0.0, 1e-6);

    CHECK_DONE();
}
