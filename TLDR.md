# TL;DR — Soft Body Manipulation (My Thought Process)

### Overview
I wanted to understand how soft, squishy objects deform and recover when handled. I picked a standard foam stress ball because its spherical shape makes the contact area clean to track, and open-cell foam makes it easy to observe how trapped air squeezes out of the material.

### My Testing Approach
Instead of complicated lab machinery, I kept the setup grounded and practical. I placed a light wooden board over the ball, stacked weights on top step-by-step, and measured how flat it got and how much it bulged sideways. To figure out how fast it snaps back, I recorded the release in high frame rate video and counted the frames.

### Through the Problem

1. **Realizing Basic Spring Rules Don't Work:**
My first thought was whether a standard spring formula ($F=kx$) would work here. But looking at the squish, it quickly became clear that it wouldn't. The ball gets noticeably stiffer the harder you press. If I used a basic linear spring formula, heavy weights would mathematically predict the ball crushing past zero height into negative space, which makes no physical sense.

2. **Finding the Physical Limit:**
I realized there is a hard stop to how flat the ball can actually get. At a certain point, all the trapped air is completely pushed out, and you are left squeezing solid plastic struts flattened against each other. Once that happens, the ball simply refuses to compress any further. That's why I used a model that flattens out at that exact physical solid limit (~9.5 mm).

3. **Noticing Where the Squish Goes:**
I expected the ball to bulge outward significantly on the sides when squeezed flat, similar to solid rubber. But looking closely, it barely grew sideways at all (2.5 mm max). This made it clear that almost all the volume loss comes from air escaping the pores, rather than the material pushing outward ($\nu \approx 0.10$).

4. **Watching the Recovery:**
When releasing the load, I checked to see if the ball bounces or overshoots its shape. Watching the video frame-by-frame showed no bounce at all. It just smoothly relaxes back to its full round shape in a fraction of a second. That meant I could model the spring-back as a smooth, heavily damped return ($c \approx 60\text{--}75\text{ Ns/m}$).

### Simulation Integration
I took this step-by-step logic and built it into my Python script (`3d_visual.py`). It simulates the ball flattening under weight, updates a visual map of the internal strain, and animates the smooth spring-back when released.
