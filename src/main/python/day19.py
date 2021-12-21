import fileinput
from collections import deque, defaultdict
from functools import reduce
from math import hypot
from operator import mul
from typing import List, Deque, Dict, Tuple

# --- Day 19: Beacon Scanner ---
# --- Part one ---

sample_input = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".split(
    "\n"
)


class Beacon:
    def __init__(self, x: int, y: int, z: int, beacon_id: int):
        self.x = x
        self.y = y
        self.z = z
        self.id = beacon_id
        self.relatives = {}

    def align(self, other_beacon: "Beacon"):
        dx = abs(self.x - other_beacon.x)
        dy = abs(self.y - other_beacon.y)
        dz = abs(self.z - other_beacon.z)
        self.relatives[other_beacon.id] = other_beacon.relatives[self.id] = ",".join(
            [str(_) for _ in [hypot(dx, dy, dz), max(dx, dy, dz), min(dx, dy, dz)]]
        )

    def compare(self, other_beacon: "Beacon"):
        result = []
        # print(f"self.relatives.keys() {self.relatives.keys()} - other_beacon.relatives {other_beacon.relatives.keys()}")
        for k in self.relatives.keys():
            if k in other_beacon.relatives:
                result.append([other_beacon.relatives[k], self.relatives[k], k])
        return result


b1 = Beacon(1, 2, 3, 0)
b2 = Beacon(4, 5, 6, 1)
b3 = Beacon(7, 8, 9, 1)
b1.align(b2)
b1.align(b1)
assert b1.compare(b2) == [["5.196152422706632,3,3", "0.0,0,0", 0]]
assert b1.compare(b1) == [
    ["5.196152422706632,3,3", "5.196152422706632,3,3", 1],
    ["0.0,0,0", "0.0,0,0", 0],
]


class Scanner:
    def __init__(self, scanner_id: int):
        self.beacons = []
        self.id = scanner_id
        self.position = {"x": 0, "y": 0, "z": 0}

    def add_beacon(self, x: int, y: int, z: int):
        new_beacon = Beacon(x, y, z, beacon_id=len(self.beacons))
        for beacon in self.beacons:
            beacon.align(new_beacon)
        self.beacons.append(new_beacon)

    def compare(self, other_scanner: "Scanner"):
        for other_scanner_beacon in other_scanner.beacons:
            for self_scanner_beacon in self.beacons:
                intersection = other_scanner_beacon.compare(self_scanner_beacon)
                if len(intersection) >= 11:
                    return other_scanner_beacon, self_scanner_beacon, intersection

    def align(self, other_scanner: "Scanner", intersections):
        for i in intersections:
            print(i)


class Solver:
    def __init__(self, dat: List[str]):
        self.scanners: List = Solver.fill(dat)

    @staticmethod
    def fill(dat):
        scanners: List = []
        scanner = None
        for line in dat:
            if "---" in line:
                if scanner:
                    scanners.append(scanner)
                scanner = Scanner(scanner_id=int(line.split()[2]))
            elif line.strip():
                beacon_data = [int(_) for _ in line.split(",")]
                scanner.add_beacon(x=beacon_data[0], y=beacon_data[1], z=beacon_data[2])
        return scanners

    def align(self):
        locked = set()
        while len(locked) < len(self.scanners):
            for idx1, scanner1 in enumerate(self.scanners):
                for idx2, scanner2 in enumerate(self.scanners):
                    if idx1 == idx2:  # or idx1 not in locked or idx2 in locked:
                        print(f"idx1 {idx1} idx2 {idx2} locked {locked}")
                        continue

                    intersection = scanner1.compare(scanner2)
                    print(intersection)

                    if not intersection:
                        continue

                    scanner1.align(scanner2, intersection)
                    locked.add(idx2)


solver = Solver(sample_input)
solver.align()

# class Scanner:
#     def __init__(self, dat: List[str]):
#         self.dat: Dict[list] = self.fill(dat)
#
#     @staticmethod
#     def fill(dat):
#         scanner = defaultdict(list)
#         count = None
#         for line in dat:
#             if "---" in line:
#                 count = int(line.split()[2])
#             elif line.strip():
#                 scanner[count].append(tuple([int(_) for _ in line.split(",")]))
#         return scanner
#
#     def compare(self, other_scanner: "Scanner"):
#         for other_values in other_scanner.dat.values():
#             for self_values in self.dat.values():
#                 intersection = other_values.compare(self_values)
#
#
#
# scanner = Scanner(sample_input)
# print(scanner.dat)


# puzzle_input = [_.strip() for _ in fileinput.input()][0]
# solution_part1 = build_version_sum(puzzle_input)
#
# assert solution_part1 == 991
# print(f"solution part1: {solution_part1}")

# --- Part two ---


#
# solution_part2 = evaluate_expression(puzzle_input)
#
# assert solution_part2 == 1264485568252
# print(f"solution part2: {solution_part2}")


# def roll(v):
#     return v[0], v[2], -v[1]
#
#
# def turn(v):
#     return -v[1], v[0], v[2]
#
#
# def sequence(v):
#     for cycle in range(2):
#         for step in range(3):  # Yield RTTT 3 times
#             v = roll(v)
#             yield v  #    Yield R
#             for i in range(3):  #    Yield TTT
#                 v = turn(v)
#                 yield v
#         v = roll(turn(roll(v)))  # Do RTR
#
#
# tmp = sequence((4, -5, 9))
# print(tmp)
#
# count = 0
# for i in sorted(tmp):
#     count += 1
#     print(f"count {count} {i}")


# p = sequence((1, 1, 1))
# q = sequence((-1, -1, 1))
# for i in sorted(zip(p, q)):
#     print(i)
