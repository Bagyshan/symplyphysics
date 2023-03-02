#!/usr/bin/env python3

from symplyphysics import (
    Eq, units, convert_to, SI, solve, expr_to_quantity
)
from symplyphysics.laws.waves import frequency_from_velocity as doppler_law

# This example show usefulness of Doppler law.
## Doppler effect is widely used in systems like radars. This effect is applicable not only to waves emitted by source, but also to waves reflected by it.
## So radar emits wave with known frequancy and then receives reflected wave with frequency modified according to Doppler's effect.
## Then radar system can calculate velocity of object. Radars may use sound waves (ultrasonic), radio or infrared (electromagnetic).
## So for example ultrasonic radar emits 40000Hz wave. An object reflects this wave and at some moment radar receives this signal.
## We can calculate object's velocity.

sound_velocity = units.Quantity('sound_velocity')
SI.set_quantity_dimension(sound_velocity, units.velocity)
SI.set_quantity_scale_factor(sound_velocity, 340 * units.meter/units.second)

# Zero velocity we are going to use as a velocity of radar related to air.
zero_velocity = units.Quantity('zero_velocity') 
SI.set_quantity_dimension(zero_velocity, units.velocity)
SI.set_quantity_scale_factor(zero_velocity, 0)

emitter_frequency = units.Quantity('emitter_frequency')
SI.set_quantity_dimension(emitter_frequency, units.frequency)
SI.set_quantity_scale_factor(emitter_frequency, 40000 * units.hertz)

# Choose any frequency and obtain the result
signal_frequency = units.Quantity('signal_frequency')
SI.set_quantity_dimension(signal_frequency, units.frequency)
SI.set_quantity_scale_factor(signal_frequency, 41200 * units.hertz)

solution = solve(doppler_law.law, doppler_law.source_velocity, dict=True)[0][doppler_law.source_velocity]

applied_solution = solution.subs({doppler_law.observed_frequency: signal_frequency,
                                  doppler_law.real_frequency: emitter_frequency,
                                  doppler_law.wave_velocity:sound_velocity,
                                  doppler_law.observer_velocity:zero_velocity
                                  })

result_velocity = expr_to_quantity(applied_solution, "result_velocity")
result = convert_to(result_velocity, units.kilometer / units.hour).subs({units.kilometer / units.hour: 1}).evalf(3)
if(result < 0):
    print(f"Object is moving towards radar with {-result} km/h velocity")
else:
    if(result == 0):
        print(f"Object is not moving")        
    else:    
        print(f"Object is moving away from radar with {result} km/h velocity")