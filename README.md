# Soft Object Deformation & Recovery Modeling

## 1. Test Subject & Physical Motivation

### 1.1 Object Selection
The primary test subject selected for this study is a standard **70 mm diameter open-cell polyurethane (PU) foam stress ball** ($m = 40.0\text{ g}$).
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/883563be-c3ce-4d63-92e3-2874d4fe4931" />

### 1.2 Why This Object?
* **Easy Geometry:** A sphere starts contact at a single point, making it simple to track how the contact area flattens.
* **Same from All Directions (Isotropic):** It squishes identically no matter which side faces up.
* **Durable & Availability:** Can be tested hundreds of times without permanent deformation and readily available in market

---

## 2. Material Properties & Quick Tests

### 2.1 Specimen Stats

| Property | Value | Notes / Method |
| :--- | :---: | :--- |
| **Mass ($m$)** | $40.0\text{ g}$ | Product specification from Amazon |
| **Diameter ($H_0$)** | $70.0\text{ mm}$ | Product specification from Amazon |
| **Radius ($R_0$)** | $35.0\text{ mm}$ | Half of diameter |
| **Exam Board Mass** | $300.0\text{ g}$ | Tare weight added for load tests |

### 2.2 Proof of Open-Cell Foam An internal uniformity
* **Visual Inspection:** Cut open a twin specimen to confirm uniform internal structure
  <img width="1920" height="1080" alt="photo_2026-11-10_15-17-18" src="https://github.com/user-attachments/assets/8e08e0b2-56e0-488f-a0cb-585453d22e15" />

## 3. Core Modeling Assumptions

1. **Continuous Material:** Modeled as a smooth, isotropic continuum.
2. **Uniform Internal Porosity:** Microscopic open pores are assumed to be homogeneously distributed throughout the entire volume of the ball.
3. **Non-Uniform Vertical Strain Field:** Compressive strain is non-uniform along the vertical height $Z$ (concentrating higher near contact boundaries and decaying into the central core).
4. **Symmetric Radial Expansion:** At any given height $Z$, horizontal expansion occurs uniformly in all radial directions across the X–Y plane.
5. **Lumped Viscoelasticity:** Pneumatic air flow drag and internal polymer matrix friction are combined into a single macroscopic damping coefficient ($c$).
6. **Overdamped Recovery:** The ball returns smoothly to its resting height ($70\text{ mm}$) without oscillating or overshooting.
---

## 4. Full Experiment 

### 4.1. Experimental Setup
1. **Load:** 2x 1kg, 2kg, 5kg to get the accurate force given, F = mg
2. **Plane board:** Equally distribute the force all over the ball
3. **Measurement scale:** To measure the displacement due to the force
4. **Glue:** To fix the position of the ball at one point
<img width="2560" height="1920" alt="image" src="https://github.com/user-attachments/assets/b393f5ea-9de1-466c-8e05-a3eb186d7e54" />

### 4.2. Experimental Procedure
1. Fix the ball to the origin of the point of the graph So it will hold steady and will not move in the experiment
2. Slowly load the masses on the board and press it against the board To find out, Force vs displacement
3. Measure The compression of the ball by measuring the distance between the datum and the board
4. Process the video in any kind of media player to measure the number of frames between the compression state of the ball to the relaxed state of the ball

### 4.2. Experimental Dataset
Includes the $0.30\text{ kg}$ wooden exam board tare mass added to each load step ($F = \text{Total Load} \cdot g$):

| Total Applied Load (kg) | Force $F$ (N) | Measured Height $y$ (mm) | Squish $\Delta z$ (mm) | Side Bulge $\Delta r$ (mm) |
| :---: | :---: | :---: | :---: | :---: |
| **0.00** | 0.00 | 70.0 | 0.0 | 0.00 |
| **1.30** | 12.75 | 51.0 | 19.0 | +0.90 |
| **2.30** | 22.56 | 46.0 | 24.0 | +1.20 |
| **3.30** | 32.37 | 40.5 | 29.5 | +1.50 |
| **4.30** | 42.18 | 35.0 | 35.0 | +1.80 |
| **5.30** | 52.00 | 25.0 | 45.0 | +2.20 |
| **6.30** | 61.80 | 22.0 | 48.0 | +2.40 |
| **7.30** | 71.61 | 19.0 | 51.0 | +2.50 |
| **8.30** | 81.42 | 12.0 | 58.0 | +2.50 |
| **9.30** | 91.23 | 10.0 | 60.0 | +2.50 |
| **10.30** | 101.04 | 9.5 | 60.5 | +2.50 |
| **11.30** | 110.85 | 9.0 | 61.0 | +2.50 |
| **12.30** | 120.66 | 9.0 | 61.0 | +2.50 |
| **13.30** | 130.47 | 9.5 | 60.5 | +2.50 |
| **14.30** | 140.28 | 9.5 | 60.5 | +2.50 |
---

### 4.2.1. Experimental Dataset Plot

<img width="1600" height="954" alt="image" src="https://github.com/user-attachments/assets/a8313d94-3905-4457-86e2-ad9a3e752f78" />


## 5. Parameter Identification

### 5.1 Non-Linear Viscoelasticity 
A single linear elastic model ($F = k \Delta z$) cannot accurately characterize open-cell polyurethane (PU) foam over large deformations:

* **Moderately Stiffening Response:** Between 1.30 kg and 4.30 kg ($50\%$ strain), the secant stiffness increases by 80% (from 671.1 N/m to 1205.1 N/m). This non-linearity is a combined result of internal cellular strut bending and non-linear geometric contact expansion as the sphere flattens against rigid plates.
---

### 5.2 Secant Stiffness Calculation Across Experimental Dataset

To observe how stiffness evolves with displacement, the effective secant stiffness $k_{\text{sec}} = F / \Delta z$ is calculated for every data point using total applied load ($M_{\text{total}} = M_{\text{load}} + 0.30\text{ kg}$ board tare mass) and force $F = M_{\text{total}} \cdot g$:

| Total Applied Load (kg) | Force $F$ (N) | Measured Height $y$ (mm) | Squish $\Delta z$ (mm) | Squish $\Delta z$ (m) | Calculated $k_{\text{sec}} = F / \Delta z$ (N/m) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1.30** | 12.75 | 51.0 | 19.0 | 0.0190 | 671.1 |
| **2.30** | 22.56 | 46.0 | 24.0 | 0.0240 | 940.0 |
| **3.30** | 32.37 | 40.5 | 29.5 | 0.0295 | 1097.3 |
| **4.30** | 42.18 | 35.0 | 35.0 | 0.0350 | 1205.1 |
| **5.30** | 52.00 | 25.0 | 45.0 | 0.0450 | 1155.6 |
| **6.30** | 61.80 | 22.0 | 48.0 | 0.0480 | 1287.5 |
| **7.30** | 71.61 | 19.0 | 51.0 | 0.0510 | 1404.1 |
| **8.30** | 81.42 | 12.0 | 58.0 | 0.0580 | 1403.8 |
| **9.30** | 91.23 | 10.0 | 60.0 | 0.0600 | 1520.5 |
| **10.30** | 101.04 | 9.5 | 60.5 | 0.0605 | 1670.1 |
| **11.30** | 110.85 | 9.0 | 61.0 | 0.0610 | 1817.2 |
| **12.30** | 120.66 | 9.0 | 61.0 | 0.0610 | 1978.0 |
| **13.30** | 130.47 | 9.5 | 60.5 | 0.0605 | 2156.5 |
| **14.30** | 140.28 | 9.5 | 60.5 | 0.0605 | 2318.7 |

---

### 5.3 Constitutive Model Formulations

#### 1. Baseline Elastic Stiffness ($k \approx 978\text{ N/m}$)
The average secant stiffness across the initial loading range (1.30 kg to 4.30 kg) serves as the baseline elastic modulus for low-strain kinematic solvers:
$$k = \text{mean}(671.1, 940.0, 1097.3, 1205.1) \approx \mathbf{978\text{ N/m}}$$

#### 2. Asymptotic Densification Model
Full-range vertical compression $y(M)$ is modeled via an exponential decay function bounded by the solid polymer limit ($y_{\text{min}} = 9.5\text{ mm}$):

$$y(M) = y_{\text{min}} + (H_0 - y_{\text{min}}) \cdot e^{-\lambda M}$$

* **$H_0 = 70.0\text{ mm}$:** Un-deformed initial height.
* **$y_{\text{min}} = 9.5\text{ mm}$:** Physical solid densification floor.
* **$\lambda \approx 0.266\text{ kg}^{-1}$:** Empirical mass decay coefficient.

*Physical Validation:* As applied mass $M \rightarrow \infty$, $e^{-\lambda M} \rightarrow 0$, guaranteeing that predicted height $y(M)$ asymptotically approaches $9.5\text{ mm}$ without ever going negative or over-compressing.

---

### 5.4 Poisson’s ratio

At M = 7.3 kg: ε_z = 51/70 = 0.729 and ε_r = 2.5/35 = 0.071, so ν = 0.098 ≈ 0.10.

Resolution (±0.5 mm on Δr) gives a range of roughly 0.04–0.15 at low load. The result shows that lateral expansion is small and volume is not conserved, consistent with open-cell foam where air escapes through the pores. Underwater squeezing produced bubbles, which supports open cells.

---

### 5.5 Damping Coefficient Extraction ($c = 75.0\text{ Ns/m}$)

1. **Video Restitution Tracking:** Frame-by-frame analysis of release video recorded at 59.81 fps confirmed full return to resting height ($70.0\text{ mm}$) occurring in 15 frames ($t_{\text{rec}} = 15 / 59.81 \approx 0.251\text{ s}$).
2. **System Damping Regime:** With mass $m = 0.040\text{ kg}$ and linear stiffness $k = 1120\text{ N/m}$, critical damping is:
   $$c_{\text{crit}} = 2\sqrt{km} = 2\sqrt{1120 \times 0.040} = 13.38\text{ Ns/m}$$
   The actual damping ratio is:
   $$\zeta = \frac{c}{c_{\text{crit}}} = \frac{75.0\text{ Ns/m}}{13.38\text{ Ns/m}} \approx \mathbf{5.60} \quad (\zeta \gg 1.0 \implies \mathbf{Heavily\ Overdamped})$$
3. **1st-Order Viscoelastic Relaxation:** Because the system is heavily overdamped, inertial oscillations ($m \ddot{z}$) are negligible compared to viscous drag ($c \dot{z}$). The 2nd-order ODE simplifies to a 1st-order relaxation equation:
   $$z(t) = H_0 - \Delta z_0 \cdot \exp\left(-\frac{t}{\tau}\right) \quad \text{where } \tau = \frac{c}{k}$$
4. **Parameter Calculation:** Evaluating $98\%$ restitution ($t \approx 3.75 \tau = 0.251\text{ s}$) yields a time constant $\tau \approx 0.067\text{ s}$:
   $$c = k \cdot \tau = 1120\text{ N/m} \times 0.067\text{ s} = \mathbf{75.0\text{ Ns/m}}$$
## 6. Mathematical Model & Asymptotic Predictions

### 6.1 Predicting Height for Next Load (Densification Curve)
To handle the plateau past 9 kg without predicting negative heights, the model uses an asymptotic exponential decay function:

$$y(M) = y_{\text{min}} + (H_0 - y_{\text{min}}) \cdot e^{-\lambda M}$$

* $H_0 = 70.0\text{ mm}$ (Resting Height)
* $y_{\text{min}} = 9.5\text{ mm}$ (Physical Densification Floor)
* $\lambda = 0.266\text{ kg}^{-1}$ (Fitted Mass Decay Rate)

*Result:* As load $M \rightarrow \infty$, predicted height $y(M)$ approaches $9.5\text{ mm}$ naturally, matching real-world foam behavior.

### 6.2 Overdamped Recovery ODE
The time-domain restitution trajectory follows a first-order relaxation curve:

$$z(t) = H_0 - \Delta z_0 \cdot \exp\left(-\frac{k}{c} t\right)$$

---

## 7. Interactive Python Simulations

### How to Run
```bash
# 2D Interactive Kinematics & Strain Heatmap
python stress_ball_2d.py

# 3D Volumetric Point Cloud Model
python stress_ball_3d.py
