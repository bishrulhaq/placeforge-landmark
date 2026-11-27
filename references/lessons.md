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
- The user judged the neighbours next, and in the web viewer, not in the stills: generic blocks beside a careful
  landmark read as "not sane". The named neighbours need their own pass (section 5b), and every detail has to exist
  in the viewer too: arches, windows and balcony bands as geometry, floor and mullion grids through `pf.viewer_facade`.
- A pale stone in shade under a blue sky renders grey-green. Warm the base colour beyond the photo sample and check
  the shaded side against a photo of the shaded side.
- A dolly whose look point travels past the camera swings the view into the sky halfway. Keep both look points far
  from the camera path, and pick a frame from the middle of every shot, not only its ends.
- After two detail passes the user still felt "no realism at all". More small parts were not the answer; five scene-wide
  things were (now "What makes a render read as fake" in SKILL.md). The sun stood behind the subjects, so every front
  was flat grey: a real late-afternoon position that side-lights the views changed more than any model. Tower glass
  was grey noise: a tinted mirror with one tint per tower and panes a hair out of plane made the district read as
  glass. The far city was a generated ring: 38,825 mapped buildings out to 6 km put the real skyline, the low
  districts and the coast where they are. Wide lenses tilted up made towers lean: level views with lens shift.
  Deep haze with two volume bounces is a dark wall: `look.haze_glow`, and a haze layer taller than every camera.
- Know each reference photo's date. Most licensed photos of this place were from 2010 to 2015, before the opera
  house, a re-clad hotel and a mall extension. `pf photos --dates` lists them; `refs.since` marks the old ones.
  Search by a neighbour's own name to find recent photos of it.
- A canal bank mapped as coastline that ends inside the far radius closed into a "sea" over the whole city: no people
  were placed, with no error. Watch the counts in the build log after every map change; the engine now drops such
  a polygon and says so.
- Night: an even quarter of windows lit at full power is a white checkerboard. Vary the lit share per building
  (3 to 30%), the brightness per window, keep colours warm, and give the sky a glow.
- A volume lit only by the sky is blue-grey smoke. Fountain spray needs a little emission of its own by day to stay
  white, and a narrow column: a wide faint one is a ghost.
- The web viewer capped the orbit at the horizon, so every view from street level looking up at the tower was
  flipped to an aerial one. Open each view button in `pf shot` after adding views; do not assume they work.
- Delegating the named neighbours to a second agent while the engine was reworked halved the wall time. Give it one
  file, the dated photo list and the free checks (`pf build`, `pf shot`), and render its work in Cycles yourself.
