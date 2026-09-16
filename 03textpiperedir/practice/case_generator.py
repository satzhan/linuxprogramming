"""
case_generator.py  --  builds the "Dropped Payroll Table" case files.

Usage:
    python3 case_generator.py            # default case (seed 42)
    python3 case_generator.py 7          # different case per group (seed 7)
    python3 case_generator.py 7 --reveal # instructor: print the answer chain

Creates ./case/ with:
    access.log          one-line log records (2000+ lines)
    staff.tsv           tab-separated staff directory (with # comment header)
    badges.txt          multi-line badge records separated by blank lines
    floors/floor-N.txt  noisy floor logs; one specific line matters
    statements/         many witness statement files, one matters
    groups/             plain name lists (one name per line)
"""
import os
import random
import shutil
import sys

FIRST = ["Ana", "Ben", "Carla", "Dev", "Elena", "Farid", "Gia", "Hugo", "Iris", "Jon",
         "Kira", "Luis", "Maya", "Nico", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tara",
         "Uma", "Victor", "Wen", "Ximena", "Yusuf", "Zoe", "Mateo", "Lena", "Raj", "Sofia"]
LAST = ["Chen", "Garcia", "Lee", "Patel", "Nguyen", "Smith", "Lopez", "Kim", "Silva", "Cruz",
        "Ramos", "Singh", "Khan", "Moreno", "Diaz", "Park", "Reyes", "Torres", "Ali", "Stone"]
DEPTS = ["Engineering", "Finance", "HR", "Support", "Sales", "Facilities"]
COLORS = ["Red", "Blue", "Green", "Yellow"]
LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
MODULES = ["AUTH", "DATABASE", "NETWORK", "UI", "API"]
MESSAGES = {
    "INFO": ["User logged in.", "Session started.", "Report exported.", "Connection established."],
    "WARNING": ["Login retries almost exhausted.", "DB nearing max capacity.",
                "Network latency detected.", "UI unresponsive."],
    "ERROR": ["Failed login attempt.", "DB connection lost.", "Network error.",
              "UI crashed.", "Timeout waiting for API."],
    # trap: contains the substring INFO but is a DEBUG line
    "DEBUG": ["Fetched user INFO from cache.", "DB query executed.",
              "Network packet sent.", "UI button clicked."],
}
# weights make error messages NOT equally common, so "top 5" is meaningful
ERROR_WEIGHTS = [5, 3, 2, 1, 4]

SUSPECT_IP = "10.0.3.77"
DECOY_IPS = ["10.0.3.7", "10.0.3.71", "10.0.3.177", "10.0.37.7"]
FLOOR_LINES = 300


def build(seed):
    rng = random.Random(seed)
    out = "case"
    if os.path.exists(out):
        shutil.rmtree(out)
    for d in ["floors", "statements", "groups"]:
        os.makedirs(os.path.join(out, d))

    # ---------- staff ----------
    names = [f"{f} {l}" for f in FIRST for l in LAST]
    rng.shuffle(names)
    names = names[:150]
    staff, used = [], set()
    for n in names:
        f, l = n.split()
        base = (f[0] + l).lower()
        u, k = base, 2
        while u in used:
            u, k = f"{base}{k}", k + 1
        used.add(u)
        staff.append({"name": n, "user": u, "dept": rng.choice(DEPTS),
                      "floor": rng.randint(1, 4)})

    # guarantee a username-prefix trap: a suspect whose username is a prefix of another
    with_twin = [s for s in staff if s["user"] + "2" in used]
    if not with_twin:
        s0 = staff[0]
        f0, l0 = s0["name"].split()
        same_initial = [f for f in FIRST if f[0] == f0[0] and f != f0] or [f0[0] + "ax"]
        twin = {"name": f"{same_initial[0]} {l0}", "user": s0["user"] + "2",
                "dept": "Sales", "floor": 2}
        staff.append(twin)
        used.add(twin["user"])
        with_twin = [s0]

    # ---------- suspects: 5 users on the shared lab machine ----------
    culprit = with_twin[0]
    others = [s for s in staff if s is not culprit and not s["user"].endswith("2")]
    rng.shuffle(others)
    red_not_oncall, oncall_not_red, plain1, plain2 = others[:4]
    suspects = [culprit, red_not_oncall, oncall_not_red, plain1, plain2]
    rng.shuffle(suspects)

    for s in staff:
        s["color"] = rng.choice(["Blue", "Green", "Yellow"])  # red assigned deliberately
        s["clearance"] = rng.randint(1, 5)
        s["badge"] = f"B-{rng.randint(1000, 9999)}"
    culprit["color"] = "Red"
    red_not_oncall["color"] = "Red"
    # sprinkle other red badges outside the suspect pool
    pool = [s for s in staff if s not in suspects]
    extra_red = rng.sample(pool, 20)
    for s in extra_red:
        s["color"] = "Red"

    # ---------- groups ----------
    oncall = {culprit["name"], oncall_not_red["name"]}
    # other on-call people, several of them red, so badge alone is not enough
    oncall |= {s["name"] for s in extra_red[:6]}
    oncall |= {s["name"] for s in rng.sample(pool, 15)}
    groups = {
        "oncall.txt": oncall,
        "coffee-club.txt": {s["name"] for s in rng.sample(staff, 40)},
        "vpn-users.txt": {s["name"] for s in rng.sample(staff, 60)} | {red_not_oncall["name"]},
        "db-admins.txt": {s["name"] for s in rng.sample(staff, 10)} | {culprit["name"], plain1["name"]},
    }
    for fname, members in groups.items():
        lst = sorted(members)
        rng.shuffle(lst)  # unsorted on purpose: comm needs sorted input
        with open(os.path.join(out, "groups", fname), "w") as fh:
            fh.write("\n".join(lst) + "\n")

    # ---------- staff.tsv ----------
    with open(os.path.join(out, "staff.tsv"), "w") as fh:
        fh.write("# Staff directory -- exported from HR system\n")
        fh.write("# Columns (TAB separated): Name, Username, Department, Floor\n")
        fh.write("#\n")
        rows = staff[:]
        rng.shuffle(rows)
        for s in rows:
            fh.write(f"{s['name']}\t{s['user']}\t{s['dept']}\t{s['floor']}\n")

    # ---------- badges.txt ----------
    with open(os.path.join(out, "badges.txt"), "w") as fh:
        rows = staff[:]
        rng.shuffle(rows)
        for s in rows:
            fh.write(f"Badge: {s['badge']}\nHolder: {s['name']}\nDept: {s['dept']}\n"
                     f"Color: {s['color']}\nClearance: {s['clearance']}\n\n")

    # ---------- floors + statements ----------
    guard_floor = rng.randint(1, 4)
    guard_line = rng.randint(120, 280)
    stmt_ids = rng.sample(range(1000, 9999), 400)
    guard_stmt = stmt_ids[0]
    decoy_stmts = stmt_ids[1:]
    fillers = ["Plant watered.", "Printer jammed again.", "Desk empty.",
               "Coffee machine descaled.", "Window left open.", "Chair reported squeaky."]
    for fl in range(1, 5):
        lines = []
        for i in range(1, FLOOR_LINES + 1):
            if fl == guard_floor and i == guard_line:
                lines.append(f"Desk {i}: Night guard shift log. SEE STATEMENT #{guard_stmt}")
            elif rng.random() < 0.45:
                lines.append(f"Desk {i}: {rng.choice(fillers)} SEE STATEMENT #{rng.choice(decoy_stmts)}")
            else:
                lines.append(f"Desk {i}: {rng.choice(fillers)}")
        with open(os.path.join(out, "floors", f"floor-{fl}.txt"), "w") as fh:
            fh.write("\n".join(lines) + "\n")

    decoy_text = ["Nothing unusual tonight.", "Heard the elevator, nobody came out.",
                  "Cleaning crew finished early.", "Someone left a red scarf in the lobby.",
                  "I was on break, sorry."]
    for sid in decoy_stmts:
        with open(os.path.join(out, "statements", f"statement-{sid}"), "w") as fh:
            fh.write(rng.choice(decoy_text) + "\n")
    with open(os.path.join(out, "statements", f"statement-{guard_stmt}"), "w") as fh:
        fh.write("Night guard statement.\n"
                 "Right after the alarm someone hurried out of the shared lab.\n"
                 "I only saw them from behind, but the badge on their lanyard was RED, no doubt.\n"
                 "They were on the phone complaining that they were stuck on call tonight.\n")

    # ---------- access.log ----------
    records = []
    ips_normal = [f"10.0.{rng.randint(0, 9)}.{rng.randint(2, 250)}" for _ in range(60)]
    ips_normal = [ip for ip in ips_normal if ip != SUSPECT_IP] + DECOY_IPS
    for _ in range(2000):
        h = rng.choices(range(24), weights=[1]*8 + [6, 8, 9, 7, 5, 7, 9, 8, 6, 3] + [1]*6)[0]
        t = h * 3600 + rng.randint(0, 3599)
        lvl = rng.choice(LEVELS)
        if lvl == "ERROR":
            msg = rng.choices(MESSAGES["ERROR"], weights=ERROR_WEIGHTS)[0]
        else:
            msg = rng.choice(MESSAGES[lvl])
        s = rng.choice(staff)
        records.append((t, lvl, rng.choice(MODULES), s["user"], rng.choice(ips_normal), msg))
    # suspects' activity on the shared machine (several lines each)
    for s in suspects:
        for _ in range(rng.randint(2, 5)):
            t = rng.randint(20 * 3600, 23 * 3600)
            records.append((t, "INFO", "AUTH", s["user"], SUSPECT_IP, "User logged in."))
    # the twin shows up from a decoy IP only
    twin_user = culprit["user"] + "2"
    records.append((22 * 3600 + 5, "INFO", "AUTH", twin_user, "10.0.3.71", "User logged in."))
    crime_t = 23 * 3600 + rng.randint(0, 1500)
    records.append((crime_t, "CRITICAL", "DATABASE", "unknown", SUSPECT_IP, "Table payroll dropped."))
    records.append((crime_t + 42, "CRITICAL", "SECURITY", "system", "0.0.0.0",
                    f"Door alarm on floor-{guard_floor}. Guard log is at line {guard_line} of that floor file."))
    records.append((rng.randint(0, 86399), "CRITICAL", "NETWORK", "system", "0.0.0.0",
                    "Disk usage above 99 percent."))
    records.sort()
    with open(os.path.join(out, "access.log"), "w") as fh:
        for t, lvl, mod, user, ip, msg in records:
            hh, mm, ss = t // 3600, (t % 3600) // 60, t % 60
            fh.write(f"[2026-09-14 {hh:02d}:{mm:02d}:{ss:02d}] [{lvl}] [{mod}] "
                     f"user={user} ip={ip}: {msg}\n")

    return {"culprit": culprit, "suspects": suspects, "floor": guard_floor,
            "line": guard_line, "stmt": guard_stmt}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    seed = int(args[0]) if args else 42
    info = build(seed)
    print(f"Case files written to ./case (seed {seed}).")
    if "--reveal" in sys.argv:
        print("\n--- INSTRUCTOR ONLY ---")
        print(f"Guard log: floor-{info['floor']}.txt line {info['line']} -> statement-{info['stmt']}")
        print("Suspects on", SUSPECT_IP + ":")
        for s in info["suspects"]:
            print(f"   {s['user']:10s} {s['name']:15s} badge={s['color']}")
        c = info["culprit"]
        print(f"Culprit: {c['name']} ({c['user']})  -- red badge AND on call")
