# Example: Lotus Tower, Colombo

The place this skill was born from. `place.json` holds the matched camera, the Colombo region settings and the
compare regions; `landmark.py` is the full tower (podium, shaft, calyx, three tiers of petals, cap, mast, antenna,
night lighting).

```bash
pf init lotus --name "Lotus Tower" --lat 6.92703 --lon 79.85828 --radius 900 --height 351.5
cp examples/lotus-tower/place.json examples/lotus-tower/landmark.py lotus/
# put your reference photos in lotus/refs/ ; the target used here is "Lotus_Tower_in_(2021).jpg" (Wikimedia Commons)
pf map lotus && pf assets lotus
pf build lotus                      # BUILD OK
pf web lotus && pf shot lotus photo # the Three.js page
pf render lotus --name loop01 --view photo,bud,drone
pf compare lotus loop01_photo
```

Reference photos are not included: they belong to their photographers.
