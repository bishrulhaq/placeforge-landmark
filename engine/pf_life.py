"""placeforge engine, life: traffic on the real streets, parked cars, people walking, trains on the running lines.

Recognisable things are never hand-built boxes: they are downloaded models (assets/assets.json, fetched by
`pf assets`). No model file, no object: the scene stays empty of that kind rather than showing a placeholder.

Every mover's place is a pure function of film time, so frames can render in any order on any machine:
    vehicles keep to their side of the road (region.drive), one speed per lane, looping along the street;
    walkers slide along footways and pavements while their mesh steps through poses baked from the walk action.
"""
import bpy, bmesh, json, math, os, random
from mathutils import Vector, Matrix
import pf_core as pf
import pf_city as city
from pf_core import cfg

POSES = 6


def load_model(path, name, coll, yaw=90.0, length=None, height=None, action=None, frame=None):
    """Import a GLB as one mesh object in the engine's convention: +X forward, +Z up, metres, origin on the ground
    under its middle. action / frame pose a rigged model before it is flattened. Returns None if it cannot load."""
    before = set(bpy.data.objects)
    try:
        bpy.ops.import_scene.gltf(filepath=path)
    except Exception as e:
        pf.log("model import failed:", os.path.basename(path), e)
        return None
    new = [o for o in bpy.data.objects if o not in before]
    if action:
        for o in new:
            if o.type == "ARMATURE":
                act = next((a for a in bpy.data.actions if action.lower() in a.name.lower()), None)
                if act:
                    if not o.animation_data:
                        o.animation_data_create()
                    o.animation_data.action = act
                    try:
                        o.animation_data.action_slot = act.slots[0]
                    except Exception:
                        pass
        bpy.context.scene.frame_set(int(frame or 1))
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    parts, mats = [], []
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in new:
        if o.type != "MESH" or o.name.lower().startswith("icosphere"):      # the importer's bone-shape helper
            continue
        me = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
        me.transform(o.matrix_world)
        idx = []
        for m in me.materials:
            if m not in mats:
                mats.append(m)
            idx.append(mats.index(m))
        parts.append((me, [idx[p.material_index] if idx else 0 for p in me.polygons]))
        for v in me.vertices:
            lo, hi = Vector(map(min, lo, v.co)), Vector(map(max, hi, v.co))
    if not parts:
        for o in new:
            bpy.data.objects.remove(o, do_unlink=True)
        return None
    bm = bmesh.new()
    for me, _ in parts:
        bm.from_mesh(me)
    out = bpy.data.meshes.new(name)
    bm.to_mesh(out)
    bm.free()
    k = 0
    for me, mi in parts:
        for i in mi:
            out.polygons[k].material_index = i
            k += 1
    size = hi - lo
    sc = height / max(size.z, 1e-6) if height else (length / max(size.x, size.y, 1e-6) if length else 1.0)
    ctr = (lo + hi) / 2
    out.transform(Matrix.Rotation(math.radians(yaw), 4, "Z") @ Matrix.Scale(sc, 4) @ Matrix.Translation((-ctr.x, -ctr.y, -lo.z)))
    for m in mats:
        out.materials.append(m)
    for me, _ in parts:
        bpy.data.meshes.remove(me)
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)
    ob = bpy.data.objects.new(name, out)
    coll.objects.link(ob)
    return ob


class Life:
    def __init__(self):
        self.cars, self.walkers, self.trains = [], [], []

    def update(self, f, t):
        for o, p, L, s0, v, off, z in self.cars:
            x, y, a = city.walk(p, (s0 + v * t) % L)
            o.location = (x - math.sin(a) * off, y + math.cos(a) * off, z)
            o.rotation_euler = (0, 0, a)
        for o, p, L, s0, v, off, poses, ph in self.walkers:
            s = (s0 + abs(v) * t) % L
            x, y, a = city.walk(p, s if v > 0 else L - s)
            o.location = (x - math.sin(a) * off, y + math.cos(a) * off, 0.16)
            o.rotation_euler = (0, 0, a if v > 0 else a + math.pi)
            o.data = poses[int((t * 1.9 + ph) * POSES) % POSES]
        for o, p, L, s0, v in self.trains:
            x, y, a = city.walk(p, (s0 + v * t) % L)
            o.location = (x, y, 0.30)
            o.rotation_euler = (0, 0, a)

    def export(self):
        return None


def build(mp, rng):
    p = os.path.join(pf.PROJECT, "assets", "assets.json")
    if not os.path.exists(p):
        pf.log("life: no assets/assets.json (pf assets): no vehicles or people")
        return None
    spec = json.load(open(p)).get("models", {})
    have = {k: m for k, m in spec.items() if os.path.exists(os.path.join(pf.PROJECT, "assets", "models", m["file"]))}
    if not have:
        pf.log("life: no model files yet (pf assets): no vehicles or people")
        return None
    kv, kp = float(cfg("life.vehicles", 0.6)), float(cfg("life.people", 0.5))
    protos = pf.collection("life_protos", hidden=False)
    coll = pf.collection("life")
    by_role = {}
    for k, m in have.items():
        path = os.path.join(pf.PROJECT, "assets", "models", m["file"])
        if m["role"] == "person":
            poses = []
            for i in range(POSES):
                o = load_model(path, "life_p_%s_%d" % (k, i), protos, m.get("yaw", 90), height=m.get("height", 1.7), action=m.get("action", "walk"), frame=1 + i * 4)
                if o:
                    poses.append(o.data)
            if len(poses) == POSES:
                by_role.setdefault("person", []).append(poses)
        else:
            o = load_model(path, "life_m_" + k, protos, m.get("yaw", 90), length=m.get("length"))
            if o:
                by_role.setdefault(m["role"], []).append(o.data)
    bpy.context.view_layer.layer_collection.children[protos.name].exclude = True
    L_ = Life()
    side = -1.0 if cfg("region.drive", "right") == "right" else 1.0       # offset to the left of travel is positive
    cars = by_role.get("car", []) + by_role.get("van", [])
    n = 0
    if cars and kv > 0:
        for r in mp.drive:
            Lr = city.length(r["p"])
            if Lr < 80 or r["w"] < 5:
                continue
            big = r["k"] in city.BIG
            lanes = [(r["p"], side * r["w"] / 4 if not r["oneway"] else 0.0)]
            if not r["oneway"]:
                lanes.append((r["p"][::-1], side * r["w"] / 4))
            for path, off in lanes:
                v = rng.uniform(9, 13) if big else rng.uniform(5, 8)
                s = rng.uniform(0, 40)
                while s < Lr - 10 and n < 1800:
                    x, y, _ = city.walk(path, s)
                    if x * x + y * y < (mp.R * 1.05) ** 2 and rng.random() < kv:
                        data = rng.choice(by_role["bus"]) if (big and by_role.get("bus") and rng.random() < 0.07) else rng.choice(cars)
                        o = bpy.data.objects.new("life_car", data)
                        coll.objects.link(o)
                        L_.cars.append((o, path, Lr, s, v, off, 0.07))
                        n += 1
                    s += rng.uniform(14, 50) / max(kv, 0.1) * (0.6 if big else 1.0)
        for a in mp.areas:                                        # parked cars
            if a["k"] != "parking" or a["far"]:
                continue
            cx, cy, w, d, rot = city.obb(a["p"])
            c, s_ = math.cos(rot), math.sin(rot)
            u = -w / 2 + 2.0
            while u < w / 2 - 1.5 and n < 2600:
                for vrow in ([-d / 2 + 3.0, d / 2 - 3.0] if d > 12 else [0.0]):
                    x, y = cx + u * c - vrow * s_, cy + u * s_ + vrow * c
                    if rng.random() < 0.6 and city.inside(a["p"], x, y) and not mp.in_building(x, y):
                        o = bpy.data.objects.new("life_parked", rng.choice(cars))
                        o.location, o.rotation_euler = (x, y, 0.04), (0, 0, rot + math.pi / 2 + (math.pi if rng.random() < 0.5 else 0))
                        coll.objects.link(o)
                        n += 1
                u += 2.7
    np_ = 0
    if by_role.get("person") and kp > 0:
        near = min(mp.R, 600.0)
        paths = [(r["p"], 0.0) for r in mp.roads if r["foot"] and city.length(r["p"]) > 25]
        paths += [(r["p"], sd * (r["w"] / 2 + 1.05)) for r in mp.drive if r["k"] not in ("motorway", "trunk") for sd in (1, -1)]
        for path, off in paths:
            Lp, s = city.length(path), rng.uniform(0, 30)
            while s < Lp - 2 and np_ < 900:
                x, y, a = city.walk(path, s)
                px, py = x - math.sin(a) * off, y + math.cos(a) * off
                if px * px + py * py < near * near and rng.random() < kp and not mp.in_water(px, py) and not mp.in_building(px, py):
                    poses = rng.choice(by_role["person"])
                    o = bpy.data.objects.new("life_walker", poses[0])
                    coll.objects.link(o)
                    L_.walkers.append((o, path, Lp, s, rng.choice((1, -1)) * rng.uniform(1.1, 1.5), off + rng.uniform(-0.5, 0.5), poses, rng.random()))
                    np_ += 1
                s += rng.uniform(12, 45) / max(kp, 0.1)
    nt = 0
    if by_role.get("loco") and by_role.get("coach"):
        for i, tr in enumerate(mp.tracks[:4:2]):
            Lt = city.length(tr["p"])
            if Lt < 300:
                continue
            s0 = rng.uniform(0, Lt)
            for k in range(6):
                o = bpy.data.objects.new("life_train", by_role["loco"][0] if k == 0 else by_role["coach"][0])
                coll.objects.link(o)
                L_.trains.append((o, tr["p"], Lt, s0 - k * 20.4, 11.0))
            nt += 1
    L_.update(1, 0.0)
    pf.log("life: %d vehicles, %d people, %d trains (models: %s)" % (n, np_, nt, ", ".join(sorted(have))))
    return L_
