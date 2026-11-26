# placeforge-landmark

**Rebuild a real place in 3D from photos, a map pin and a radius.**

placeforge-landmark is a skill for [Claude Code](https://claude.com/claude-code). You give it reference photos of a place,
where it is on the map and how many metres around it you want. It builds the place in Blender on real
OpenStreetMap data, models the landmark from your photos, and then improves the result in a loop: render, compare
with the photo by numbers and by eye, fix the worst gap, render again.

From one scene description you get:

- **Stills** in Blender Cycles, matched to your reference photo
- **A film** of any length: day, sunset and night, with traffic, people and trains moving
- **An interactive Three.js page** (one HTML file) with orbit controls and a time-of-day slider

It was born from rebuilding the Lotus Tower in Colombo, which ships as the worked example.

## What you need

- [Claude Code](https://claude.com/claude-code)
- [Blender](https://www.blender.org/download/) 4.2 or newer (tested with 5.2), Python 3.9+, `pip install pillow`
- For films: `ffmpeg`. For viewer screenshots: Chrome and `pip install websocket-client`
- A place to render: your own GPU or CPU, **or** a rented GPU on [Vast.ai](https://vast.ai) (about $0.30 to $0.50
  an hour for an RTX 4090), **or** any Linux machine you can reach over SSH

## Install

```bash
git clone https://github.com/bishrulhaq/placeforge-landmark ~/.claude/skills/placeforge-landmark
```

Then ask Claude Code:

> Rebuild the Lotus Tower in Colombo from the photos in ~/Pictures/lotus. 900 m radius. I want a still, a 30 second
> film and a web page.

Claude asks for anything missing (photos, the pin, the radius, the outputs, where to render), then works through
the steps below.

## How it works

| Step | Command | What happens |
|---|---|---|
| Find the pin | `pf locate "Lotus Tower Colombo"` | Name, maps link or `lat,lon` to coordinates |
| Start a project | `pf init P --lat .. --lon .. --radius 900 --photos DIR` | `place.json`, `.env`, `landmark.py` |
| Real map | `pf map P` | Streets, footprints, heights, water, coast, railways, parks, trees inside the radius |
| Read the photos | `pf refs P` | Contact sheet and a pixel grid on the target photo |
| Match the camera | `pf camera P --horizon .. --base-row .. --top-row ..` | Camera distance, height, lens and compass from one photo |
| Model the landmark | edit `P/landmark.py` | The one hand-made part, measured from the photos |
| Loop | `pf render`, `pf compare`, `pf log` | Render, compare, fix the worst gap, again |
| Film | `pf film plan / render / encode` | Shots in a JSON file; frames; MP4 with fades and music |
| Web | `pf web P` | Blender to Three.js: `P/web/index.html` |

The loop is recursive: wide view first, then the district, the landmark, the street, a single detail; each level
sends fixes back to the one scene description. And each finished project adds its lessons to
`references/lessons.md`, which the skill reads before the next place.

## Where renders run

Copy `.env.example` to `.env` in your project (`pf init` does it) and choose:

```ini
PF_COMPUTE=local      # this machine: Apple Metal, NVIDIA OptiX/CUDA, AMD HIP, Intel oneAPI, else the CPU
PF_COMPUTE=vast       # rent a GPU by the hour: add VAST_API_KEY and VAST_MAX_PRICE
PF_COMPUTE=ssh        # a machine you already have: add PF_SSH_HOST, PF_SSH_USER, PF_SSH_KEY
```

Your key never leaves `.env`. A rented machine is destroyed when the frames are down (`pf gpu P down`).

## Example

```bash
pf init lotus --name "Lotus Tower" --lat 6.92703 --lon 79.85828 --radius 900 --height 351.5
cp examples/lotus-tower/place.json examples/lotus-tower/landmark.py lotus/
pf map lotus && pf assets lotus
pf web lotus            # open lotus/web/index.html
```

## Honest limits

- The ground is flat; hilly sites need terrain, which is not built yet.
- Flyovers and tunnels are drawn at grade. Bridges over water get a deck.
- Beyond the detailed radius the city is generated, not mapped building by building.
- The landmark is modelled by Claude from your photos. Its quality depends on the photos (close-ups matter most)
  and on how many loops you let it run.
- The Three.js page has no moving traffic yet.

## Credits and licences

- Code: MIT (see `LICENSE`).
- Map data: (c) [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, ODbL. Credit it wherever you
  show a result.
- Default models: Quaternius (via Poly Pizza) and Grab3D, CC0. Ground textures: Poly Haven, CC0. The list and
  every licence: `assets.default.json`.
- Your reference photos stay yours (or their photographers'). They are references, never published by this tool.
