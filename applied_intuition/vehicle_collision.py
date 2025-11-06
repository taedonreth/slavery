"""
Vehicle Collision Detection: Discrete and Continuous Time Approaches

This module implements two approaches for detecting collisions between moving vehicles:
1. Discrete time simulation (step-by-step approximation)
2. Continuous time simulation (exact analytical solution with binary search)
"""
import math
from typing import List, Optional


# =============================================================================
# DISCRETE TIME SIMULATION
# =============================================================================
# Approximates vehicle motion by stepping through time in small increments.
# Simple to implement but accuracy depends on step size (dt).


class Car:
    """
    Represents a car moving in 2D space with circular collision boundary.
    
    The car moves in a potentially curved path based on its angular velocity.
    """
    def __init__(self, x, y, v, theta, omega, radius):
        self.x = x          # position (m)
        self.y = y
        self.v = v          # linear speed (m/s)
        self.theta = theta  # heading angle (radians): 0=right, π/2=up, π=left
        self.omega = omega  # angular velocity (rad/s): >0 turns left, <0 turns right
        self.radius = radius  # circle radius for collision detection (m)

    def update(self, dt: float):
        """
        Advance position and heading by dt seconds.
        
        MATH EXPLANATION:
        -----------------
        1. Update heading: θ_new = θ_old + ω·dt
           - If ω=0: moves straight (heading unchanged)
           - If ω>0: turns counterclockwise (left)
           - If ω<0: turns clockwise (right)
        
        2. Decompose velocity into x and y components:
           - v_x = v·cos(θ)  ← horizontal component
           - v_y = v·sin(θ)  ← vertical component
           
           Visual: 
                 * (car)
                /|
               / | v·sin(θ) ← y-component
             v/  |
             / θ |
            *----+
              v·cos(θ) ← x-component
        
        3. Update position: position_new = position_old + velocity·dt
           - This approximates the curved path with straight line segments
           - Smaller dt → more accurate approximation
        """
        # Update heading angle (turns the car)
        self.theta += self.omega * dt
        
        # Update x position: add horizontal component of velocity × time
        self.x += self.v * math.cos(self.theta) * dt
        
        # Update y position: add vertical component of velocity × time
        self.y += self.v * math.sin(self.theta) * dt


def simulate_collision(cars: List[Car], dt: float, max_time: float) -> Optional[float]:
    """
    Step through time in increments of dt until any two cars collide.
    
    COLLISION DETECTION:
    --------------------
    Two circular objects collide when their centers are closer than
    the sum of their radii:
        distance(center1, center2) ≤ radius1 + radius2
    
    ALGORITHM:
    ----------
    At each time step:
    1. Check all pairs of cars for collision
    2. If collision found, return current time
    3. If no collision, advance all cars by dt
    4. Repeat until max_time reached
    
    Args:
        cars: List of Car objects to simulate
        dt: Time step size (smaller = more accurate but slower)
        max_time: Maximum simulation time
    
    Returns:
        Time of first collision, or None if no collision within max_time
    """
    t = 0.0
    while t <= max_time:
        # Check all unique pairs of cars for collision
        # (i, j) where j > i ensures we don't check the same pair twice
        for i in range(len(cars)):
            for j in range(i + 1, len(cars)):
                # Calculate Euclidean distance between car centers
                # Distance formula: d = √[(x₁-x₂)² + (y₁-y₂)²]
                dx = cars[i].x - cars[j].x
                dy = cars[i].y - cars[j].y
                dist = math.sqrt(dx * dx + dy * dy)
                
                # Collision occurs when distance ≤ sum of radii
                # (circles touch or overlap)
                if dist <= cars[i].radius + cars[j].radius:
                    return t
        
        # No collision found, advance simulation by one time step
        for c in cars:
            c.update(dt)
        t += dt
    
    return None


# Example: Two cars on head-on collision course
# Car 1: starts at origin, moves right (θ=0) at 1 m/s
# Car 2: starts at x=5, moves left (θ=π) at 1 m/s
# Both have radius 1, so they collide when centers are 2m apart
# Starting distance: 5m, closing speed: 2 m/s, gap to close: 3m
# Expected collision time: ~1.5 seconds (depending on dt accuracy)
cars = [
    Car(x=0, y=0, v=1, theta=0, omega=0, radius=1),
    Car(x=5, y=0, v=1, theta=3.14159, omega=0, radius=1)
]
print("Discrete collision time:", simulate_collision(cars, dt=0.1, max_time=10))


# =============================================================================
# CONTINUOUS TIME SIMULATION
# =============================================================================
# Uses exact mathematical formulas for vehicle trajectories.
# More accurate and faster than discrete simulation (uses binary search).
# Key difference: computes position at ANY time t using calculus-derived formulas.


class Car:
    """
    Represents a car with analytical position formulas.
    
    Unlike discrete simulation, this computes exact position at any time t
    without stepping through intermediate times.
    """
    def __init__(self, x0, y0, v, theta0, omega, radius):
        self.x0 = x0        # initial x position (m)
        self.y0 = y0        # initial y position (m)
        self.v = v          # linear speed (m/s) - constant
        self.theta0 = theta0  # initial heading angle (radians)
        self.omega = omega  # angular velocity (rad/s) - constant
        self.radius = radius  # collision circle radius (m)

    def position(self, t: float):
        """
        Return (x, y) position at continuous time t using exact formulas.
        
        WHY TWO CASES:
        --------------
        The trajectory differs fundamentally based on angular velocity:
        - ω = 0: Car moves in a STRAIGHT LINE
        - ω ≠ 0: Car moves in a CIRCULAR ARC
        
        These require different mathematical formulas!
        """
        if abs(self.omega) < 1e-8:
            # ═════════════════════════════════════════════════════════════
            # CASE 1: STRAIGHT LINE MOTION (ω ≈ 0)
            # ═════════════════════════════════════════════════════════════
            # When not turning, heading stays constant: θ(t) = θ₀
            # 
            # Position formula: position = initial + velocity·time
            #   x(t) = x₀ + v·cos(θ₀)·t
            #   y(t) = y₀ + v·sin(θ₀)·t
            #
            # This is the same as discrete version when ω=0!
            x = self.x0 + self.v * math.cos(self.theta0) * t
            y = self.y0 + self.v * math.sin(self.theta0) * t
        else:
            # ═════════════════════════════════════════════════════════════
            # CASE 2: CIRCULAR ARC MOTION (ω ≠ 0)
            # ═════════════════════════════════════════════════════════════
            # When turning, car follows a circular path around a center point.
            #
            # TURN RADIUS: R = v/ω
            #   - Comes from circular motion physics: v = R·ω
            #   - Larger |ω| → tighter turn (smaller R)
            #   - Example: v=10 m/s, ω=1 rad/s → R=10m (tight)
            #   - Example: v=10 m/s, ω=0.1 rad/s → R=100m (wide)
            #
            # HEADING AT TIME t: θ(t) = θ₀ + ω·t
            #
            # POSITION FORMULAS (derived from integrating velocity):
            #   x(t) = x₀ + R·[sin(θ₀ + ω·t) - sin(θ₀)]
            #   y(t) = y₀ - R·[cos(θ₀ + ω·t) - cos(θ₀)]
            #
            # INTUITION: The [sin(...) - sin(...)] terms measure how far
            # the car has traveled along its circular arc in each direction.
            #
            # Visual of circular motion:
            #        * (position at time t)
            #       /
            #      /  ← follows curve, not straight line!
            #     |
            #     |  R (turn radius)
            #     |
            #     o (center of turning circle)
            #
            R = self.v / self.omega
            x = self.x0 + R * (math.sin(self.theta0 + self.omega * t) - math.sin(self.theta0))
            y = self.y0 - R * (math.cos(self.theta0 + self.omega * t) - math.cos(self.theta0))
        return x, y


def first_collision_time(c1: Car, c2: Car, t_max=100.0, tol=1e-4) -> Optional[float]:
    """
    Find earliest continuous time when two cars' circles touch.
    Uses binary search over time to find the collision moment.
    
    ALGORITHM: BINARY SEARCH FOR COLLISION TIME
    --------------------------------------------
    Goal: Find the first moment when distance ≤ radius₁ + radius₂
    
    Key Assumption: Cars start not colliding, then get closer until collision.
    We search for the boundary between "not colliding" and "colliding" states.
    
    Args:
        c1, c2: Two Car objects
        t_max: Maximum time to search (should be reasonable to avoid issues
               if cars pass through each other)
        tol: Time precision in seconds (default: 0.0001s = 0.1ms)
    
    Returns:
        Time of first collision, or None if no collision within t_max
    """
    def dist_sq(t):
        """
        Calculate SQUARED distance between car centers at time t.
        
        WHY SQUARED DISTANCE?
        ---------------------
        1. Faster: Avoids expensive sqrt() operation
        2. Comparison works: If d₁ < d₂, then d₁² < d₂²
        3. Collision check: d² ≤ (r₁+r₂)² is same as d ≤ r₁+r₂
        
        Distance formula: d² = (x₁-x₂)² + (y₁-y₂)²
        """
        x1, y1 = c1.position(t)
        x2, y2 = c2.position(t)
        return (x1 - x2)**2 + (y1 - y2)**2

    # Collision threshold: (radius₁ + radius₂)²
    # Collision occurs when dist_sq(t) ≤ r_sum_sq
    r_sum_sq = (c1.radius + c2.radius)**2
    
    # Quick check: Are cars already colliding at t=0?
    if dist_sq(0) <= r_sum_sq:
        return 0.0

    # ═════════════════════════════════════════════════════════════════════
    # BINARY SEARCH: Find the collision time
    # ═════════════════════════════════════════════════════════════════════
    # Search interval: [left, right]
    # Invariant: collision happens somewhere in [left, right] (or not at all)
    #
    # Visual of search space:
    #
    #   Time:  0 ─────────────────────────────── t_max
    #          ↑                                   ↑
    #         left                               right
    #
    # We repeatedly check the midpoint and narrow the interval by half.
    
    left, right = 0.0, t_max
    
    while right - left > tol:
        mid = (left + right) / 2
        
        # ─────────────────────────────────────────────────────────────────
        # DECISION LOGIC: Which half contains the collision?
        # ─────────────────────────────────────────────────────────────────
        
        if dist_sq(mid) < r_sum_sq:
            # Cars ARE colliding at mid
            # → Collision must have started at or before mid
            # → Search LEFT half: [left, mid]
            #
            # Example:
            #   Time:  0 ──── mid ──── t_max
            #                  ↑ (collision!)
            #          Search [0, mid] for when it started
            right = mid
        else:
            # Cars are NOT colliding at mid
            # → Collision hasn't happened yet (or doesn't happen at all)
            # → Search RIGHT half: [mid, t_max]
            #
            # Example:
            #   Time:  0 ──── mid ──── t_max
            #                  ↑ (not colliding yet)
            #          Search [mid, t_max] for collision
            #
            # WHY NOT left = mid + tol?
            # -------------------------
            # The collision could happen at mid + 0.000001 seconds!
            # If we skip ahead by tol, we might jump PAST the collision point.
            # Binary search works by keeping left just before the collision
            # and right just after, then squeezing them together.
            left = mid
    
    # ═════════════════════════════════════════════════════════════════════
    # FINAL CHECK: Verify collision at found time
    # ═════════════════════════════════════════════════════════════════════
    # After loop ends: right - left ≤ tol (very close)
    # Return 'right' if there's actually a collision, else None
    return right if dist_sq(right) <= r_sum_sq else None


# Example: Same scenario as discrete version, but with exact calculation
# Car 1: origin, moving right at 1 m/s, radius 1
# Car 2: x=5, moving left at 1 m/s, radius 1
# Expected: Exactly 1.5 seconds (no approximation error!)
c1 = Car(0, 0, 1, 0, 0, 1)
c2 = Car(5, 0, 1, math.pi, 0, 1)
print("Continuous collision time:", first_collision_time(c1, c2))


# =============================================================================
# COMPARISON: DISCRETE VS CONTINUOUS
# =============================================================================
"""
Discrete Time Approach:
-----------------------
+ Simple to implement
+ Easy to understand
+ Works with any physics model
- Accuracy depends on dt (smaller dt = more accurate but slower)
- Approximates curves with line segments
- Must step through ALL intermediate times

Continuous Time Approach:
-------------------------
+ Mathematically exact (no approximation error)
+ Fast: O(log(t_max/tol)) using binary search
+ No need to compute intermediate positions
- Requires analytical position formulas
- More complex math (integration, trig)
- Assumes constant velocity/angular velocity

When to use each:
-----------------
Discrete: Real-time simulation, complex physics, variable velocities
Continuous: Offline analysis, simple motion models, need exact results
"""


# =============================================================================
# FOLLOW-UP QUESTIONS & ANSWERS
# =============================================================================

"""
MATHEMATICAL MODELING
---------------------

Q: How exactly are you computing the car's position at time t when the car 
   has a constant turn rate?
A: Integrate velocity vector over time. With constant ω, heading θ(t) = θ₀ + ωt.
   The position formulas come from ∫v·cos(θ(t))dt and ∫v·sin(θ(t))dt, yielding
   circular arc equations with turn radius R = v/ω.

Q: What changes if acceleration is introduced instead of constant speed?
A: Velocity becomes v(t) = v₀ + at. The integrals become more complex (quadratic
   terms appear), requiring ∫∫ for position. Can't use simple R = v/ω anymore;
   need to integrate variable velocity along the curve. Often requires numerical
   methods or Euler spiral approximations.

Q: Could you express the car's motion parametrically using trigonometric functions?
A: Yes, already done! For constant ω: x(t) = x₀ + R[sin(θ₀+ωt) - sin(θ₀)],
   y(t) = y₀ - R[cos(θ₀+ωt) - cos(θ₀)]. For ω=0: x(t) = x₀ + vt·cos(θ₀),
   y(t) = y₀ + vt·sin(θ₀). Both are parametric with parameter t.


COLLISION DETECTION
-------------------

Q: Given two parametric trajectories (x₁(t), y₁(t)) and (x₂(t), y₂(t)),
   how do you check for collision (circle overlap)?
A: Compute distance d(t) = √[(x₁(t)-x₂(t))² + (y₁(t)-y₂(t))²]. Collision
   occurs when d(t) ≤ r₁ + r₂. Find minimum of d(t) or first time it crosses
   the threshold.

Q: Is there a closed-form way to solve for t, or would you use numerical
   approximation?
A: For straight-line motion, you can solve the quadratic equation for d²(t).
   For circular motion (with trig functions), no general closed form exists.
   Use numerical methods: binary search (as shown), Newton's method, or
   root-finding algorithms.

Q: What assumptions did you make about continuous vs. discrete time, and
   what's the tradeoff?
A: Continuous assumes analytical formulas exist (constant v, ω). Discrete works
   for any model but trades accuracy for simplicity. Continuous is exact but
   rigid; discrete is approximate but flexible. Choose based on whether you
   need precision (continuous) or generality (discrete).


COMPLEXITY & ALGORITHMS
------------------------

Q: What's the time complexity of your collision detection approach?
A: Discrete: O(n²·T/dt) where n=cars, T=max_time, dt=step size.
   Continuous: O(n²·log(T/tol)) using binary search per pair.
   Continuous is much faster for fine precision.

Q: How does discretizing time steps (simulation-based approach) compare to
   solving analytically?
A: Discrete is O(T/dt) iterations; smaller dt increases cost but improves
   accuracy. Analytical is O(log(T/tol)) with exact trajectories. Analytical
   wins on speed and precision but requires closed-form solutions. Discrete
   handles complex physics that lack analytical solutions.

Q: How would you ensure numerical stability if using floating-point computations?
A: Use double precision; avoid subtracting nearly-equal numbers; use squared
   distances to avoid sqrt errors; add epsilon tolerance for comparisons;
   normalize vectors; use stable integration methods (RK4 vs Euler); check
   for NaN/infinity; clamp values to valid ranges.


EDGE CASES
----------

Q: What happens if the cars start overlapped (collision at t = 0)?
A: Both approaches handle this: discrete checks at t=0 and returns 0.0;
   continuous explicitly checks dist_sq(0) ≤ r_sum_sq and returns 0.0.

Q: What if their paths never intersect? How does your code handle "no collision"?
A: Discrete returns None after reaching max_time. Continuous returns None if
   dist_sq(right) > r_sum_sq at the end (binary search finds no collision
   within tolerance). Both correctly handle the no-collision case.

Q: What if one car has zero turn rate (straight line) and the other is curving —
   does your approach still work?
A: Yes! Each car's position is computed independently. One uses straight-line
   formula (ω≈0), the other uses circular arc formula (ω≠0). The distance
   function works regardless. The trajectories can be different types.


SYSTEM DESIGN / SCALING
------------------------

Q: Imagine scaling this to simulate thousands of cars. How would you optimize
   collision detection?
A: Spatial partitioning: divide space into grid cells or use quadtree/octree.
   Only check cars in same/adjacent cells. Reduces from O(n²) to O(n) average
   case. Use bounding boxes for quick rejection. Parallel processing for
   independent regions. Update only moving cars.

Q: Would you still compare every pair of cars, or use spatial partitioning
   (quadtrees, grids, sweep line)?
A: Use spatial partitioning (grid/quadtree) for static snapshots, or sweep-and-prune
   (sort by axis, check overlaps in 1D first). For moving objects, use
   temporal coherence: track colliding pairs from previous frame, check nearby
   objects first. Binary space partitioning for 2D scenes.

Q: How would you handle real-time constraints if this were used in an actual
   driving simulator?
A: Use discrete time with fixed dt matching frame rate (e.g., 60 FPS = dt=0.0167s).
   Spatial partitioning to reduce checks. Broad phase (AABB) + narrow phase
   (circle/polygon). Predict collisions ahead to avoid tunneling. Multi-threading:
   partition space, process regions in parallel. Lazy evaluation: only check
   cars within view distance.


PHYSICAL REALISM
----------------

Q: How would friction, acceleration, or variable turn rates complicate your math?
A: No closed-form position formulas; must use numerical integration (Euler, RK4,
   Verlet). State becomes (x, y, v, θ, a, ω_dot). Each timestep updates
   acceleration, velocity, then position. Continuous analytical approach no
   longer viable. Must use discrete simulation with physics engine.

Q: If cars can change decisions dynamically (like braking), how would you
   adjust your model to predict collisions?
A: Trajectory prediction: extrapolate current state forward assuming constant
   controls. Update predictions each frame. Use Monte Carlo simulation for
   uncertain behaviors. Compute time-to-collision (TTC) based on current
   trajectories. Recompute when state changes. Use maneuver planning to avoid
   predicted collisions.

Q: Finally, discuss how your solution would differ if the cars were running
   on a bounded circular track versus free motion in the plane.
A: Circular track: add boundary constraints, wrap coordinates (modulo track
   circumference), check for lapping (position + n·track_length). Track
   curvature affects dynamics (centripetal force, banking). 1D curvilinear
   coordinate system (arc length along track) simplifies collision to 1D
   interval overlap. Free motion: full 2D position needed, no wrapping,
   unbounded space, simpler dynamics (no track forces).
"""
