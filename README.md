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

### 5.3 Fitted Models

**Baseline stiffness (low compression):** the mean of k_sec over 1.30–4.30 kg gives

k = (671.1 + 940.0 + 1097.3 + 1205.1) / 4 = **978 N/m**

This is an effective structural stiffness (N/m), not a material modulus. It applies only for Δz ≤ 35 mm.

**Full-range height model (empirical saturating fit):**

y(M) = y_min + (H0 − y_min) · exp(−λ·M)

| Parameter | Value | Meaning |
|---|---|---|
| H0 | 70.0 mm | measured rest height |
| y_min | 9.5 mm | measured densification floor |
| λ | 0.266 kg⁻¹ | non-linear least-squares fit, M = 1.3–9.3 kg |
| RMSE | 3.8 mm | fit error over 1.3–9.3 kg |

The form is chosen because it satisfies y(0) = H0 and y(∞) = y_min, so it cannot predict negative heights. It is an empirical model, not a standard law. The fit over-predicts compression at 2.3–4.3 kg (by about 4–6 mm) and under-predicts it at 8.3–9.3 kg (by about 4–5 mm). Height resolution is about ±0.5 mm.

### 5.4 Poisson's Ratio
ν = ε_r / ε_z, with ε_z = Δz/H0 and ε_r = Δr/R0 (H0 = 70 mm, R0 = 35 mm).

| M (kg) | ε_z | ε_r | ν |
|---|---|---|---|
| 1.3 | 0.271 | 0.026 | 0.095 |
| 2.3 | 0.343 | 0.034 | 0.100 |
| 4.3 | 0.500 | 0.051 | 0.103 |
| 7.3 | 0.729 | 0.071 | 0.098 |
| 14.3 | 0.864 | 0.071 | 0.083 |

ν stays at about 0.08–0.10 across the full range. The side bulge saturates at 2.5 mm while Δz keeps growing. Lateral expansion is therefore small and volume is not conserved, consistent with open-cell foam in which air leaves through the pores (squeezing the ball underwater released bubbles). With ±0.5 mm resolution on Δr, ν at the lowest load is uncertain by roughly 0.04–0.15.

### 5.5 Damping: c ≈ 63 N·s/m (range 59–67)
**Measurement:** release video at 59.81 fps shows recovery to within 2% of rest height in 15 frames, so t_rec = 15 / 59.81 = 0.251 s (±1 frame = ±17 ms).

**Model:** the recovery shows no oscillation, so inertia is neglected and the response is first-order:

z(t) = H0 − Δz0 · exp(−t/τ), with τ = c/k

**Result:** 98% settling takes 3.91τ, so τ = 0.251 / 3.91 = 0.064 s (range 0.060–0.068 s). With k = 978 N/m:

c = k·τ = 978 × 0.064 ≈ **63 N·s/m** (range 59–67)

The damping ratio ζ = c / (2·√(k·m)) ≈ 5 (m = 0.040 kg), so the ball is heavily overdamped.


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
