# Lessons: what made each place real

Add two or three lines per finished project. Read this before starting a new place. This file is how the skill
improves from one use to the next.

## Lotus Tower, Colombo (Nov 2026; 22 loops, 3 films)

- The diff fell 927 -> 353 over ten loops; the three biggest drops were: the near city made low-rise (1 to 2
  floors, no towers within 2.5 km), the bud rebuilt from close-ups, and the haze layer lowered from 1,420 m to 820 m.
- Real map inside the radius changed what users believed: one identified building fixed the compass (bearing 355).
- Placeholders were each noticed: box cars, peg people, a blur disc casting a round shadow. Downloaded CC0 models
  replaced all of them. Liveries were painted by position in the shader over a downloaded bus body; check the
  newest photos, fleets change colour.
- Trees close up need leaf cards; clumps alone read as green boulders.
- Night: one saturated LED colour at a time, low emission strengths, no haze slab, no cloud deck.
- Film: birds without wing motion and a frozen helicopter read as fake and were cut. Star-streak flares were cut.
- People must not be decimated: at 420 triangles a walker turned to shreds. Vehicles survive 1,100.
- A rotor's hub is not its bounding-box centre (blades make the box lopsided): use the hub material's faces.
- Viewer: 58 M triangles a frame came from hundreds of downloaded vehicles in three passes; distance culling and
  keeping small things out of reflections fixed the frame rate.

## Burj Khalifa, Dubai (Nov 2026; 7 loops, 1 film, one RTX 4090 for 143 min, $0.88)

- Look in the map before modelling. OpenStreetMap carried the tower as 35 `building:part` outlines with heights, and
  they agreed with the published tier order. The model is those outlines extruded; only the pinnacle, the crowns and
  the facade shader are hand work. The same parts showed the pin was 21 m off the tower's centre: move the pin first.
- A named neighbour can be missing from the map as fetched. The Dubai Mall is a `shop=mall` relation with a few 3D
  parts inside; the fetcher dropped the whole outline. Count the big buildings a local would name against `map/preview.png`.
- A tall landmark puts cameras above the haze. That exposed three faults at once: black ground (the haze floor lay on
  the ground plane), a dark line on the horizon (the ground ended at 30 km, the sky under the horizon is dark) and a
  bright one (a haze box as large as the ground). Check a top-down view and a high orbit early.
- Desert: `region.ground` sand, exposure about half a stop under the default, clouds off, far ring dense. With the
  default exposure every roof and the ground burn to white.
- Time one frame before and after each new detail. Spray whose density varied inside the jets made every film frame
  four times slower, even off screen; one constant density gave the speed back.
- Check the direction of anything that moves against its nose. The helicopter flew tail first (a sign), and its orbit
  passed through a 370 m tower until the clearance check raised it. Judge the nose from a frame where the travel
  direction is certain (two frames a second apart), not from one still.
- Licensed photo sources gave many views from the tower and almost none of it. The match target was a night photo;
  the day look was judged by eye against close-ups. Ask for a daylight, level, whole-landmark photo at intake.
