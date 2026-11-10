# Soft Object Deformation & Recovery Modeling

## 1. Test Subject & Physical Motivation

### 1.1 Object Selection
The primary test subject selected for this study is a standard **70 mm diameter open-cell polyurethane (PU) foam stress ball** ($m = 40.0\text{ g}$).
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/883563be-c3ce-4d63-92e3-2874d4fe4931" />

### 1.2 Why This Object?
* **Easy Geometry:** A sphere starts contact at a single point, making it simple to track how the contact area flattens.
* **Same from All Directions (Isotropic):** It squishes identically no matter which side faces up.
* **Air Expulsion vs. Rubber:** Unlike solid rubber that bulges out heavily, this open-cell foam loses up to most of its volume by pushing air out of its pores.
* **Durable:** Can be tested hundreds of times without permanent deformation.

---

## 2. Material Properties & Quick Tests

### 2.1 Specimen Stats

| Property | Value | Notes / Method |
| :--- | :---: | :--- |
| **Mass ($m$)** | $40.0\text{ g}$ | Product specification from Amazon |
| **Diameter ($H_0$)** | $70.0\text{ mm}$ | Product specification from Amazon |
| **Radius ($R_0$)** | $35.0\text{ mm}$ | Half of diameter |
| **Exam Board Mass** | $300.0\text{ g}$ | Tare weight added for load tests |

### 2.2 Proof of Open-Cell Foam (Water Test)
* **Visual Inspection:** Cut open a twin specimen to confirm uniform internal pores.
  <img width="1920" height="1080" alt="photo_2026-11-10_15-17-18" src="https://github.com/user-attachments/assets/8e08e0b2-56e0-488f-a0cb-585453d22e15" />


## 3. Core Modeling Assumptions

1. **Continuous Material:** Modeled as a smooth, uniform soft body at the macro scale.
2. **Symmetric Squish:** Vertical squeezing ($Z$-axis) produces equal radial expansion sideways ($X\text{--}Y$ plane).
3. **Lumped Viscoelasticity:** Air drag and polymer friction are combined into a single damping constant ($c$).
4. **Recovery:** The ball rebounds smoothly back to shape without bouncing or overshooting past $70\text{ mm}$.

---

## 4. Experimental Data & Key Findings

### 4.1 Static Load-Deformation Test (1 kg to 14 kg)

| Load (kg) | Force (N) | Height $y$ (mm) | Squish $\Delta z$ (mm) | Side Bulge $\Delta r$ (mm) | Physical Phase |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **0.0** | 0.0 | 70.0 | 0.0 | 0.0 | Resting State |
| **1.0** | 9.8 | 51.0 | 19.0 | +0.9 | Linear Strut Bending |
| **2.0** | 19.6 | 46.0 | 24.0 | +1.2 | Linear Strut Bending |
| **3.0** | 29.4 | 40.5 | 29.5 | +1.5 | Linear Strut Bending |
| **4.0** | 39.2 | 35.0 | 35.0 | +1.8 | Linear Elastic Limit ($k \approx 1120\text{ N/m}$) |
| **5.0–8.0** | 49.1–78.5 | 25.0 ➔ 12.0 | 45.0 ➔ 58.0 | +2.2 ➔ +2.5 | Cell-Wall Collapse & Air Expulsion |
| **9.0–14.0** | 88.3–137.3 | 10.0 ➔ 9.5 | 60.0 ➔ 60.5 | +2.5 (Max) | **Densification Floor** (Solid polymer crushed flat) |

---

## 5. Parameter Identification

### 5.1 Calibrated Stiffness ($k = 1120\text{ N/m}$)
From the initial linear range ($1\text{ to } 4\text{ kg}$), the effective spring stiffness is calculated as:
$$k = \frac{F}{\Delta z} = \frac{39.24\text{ N}}{0.035\text{ m}} \approx \mathbf{1120\text{ N/m}}$$

### 5.2 Poisson's Ratio ($\nu = 0.10$)
At $50.5\text{ mm}$ vertical squish ($\varepsilon_z = 71.4\%$), the side bulge was measured at $+2.5\text{ mm}$ ($\varepsilon_r = 7.14\%$):
$$\nu = \frac{\varepsilon_r}{\varepsilon_z} = \frac{0.0714}{0.7143} \approx \mathbf{0.10}$$
*A ratio of 0.10 proves side expansion is almost negligible compared to internal void collapse.*

### 5.3 Damping Coefficient ($c = 75.0\text{ Ns/m}$)
Video analysis at 60 fps showed full recovery in 15 frames ($0.25\text{ s}$). Because the damping ratio $\zeta = \frac{c}{2\sqrt{km}} \approx 5.6 \gg 1.0$, the recovery is **heavily overdamped**. 

The relaxation time constant $\tau = \frac{c}{k} = 0.067\text{ s}$ yields:
$$c = k \cdot \tau = 1120 \times 0.067 \approx \mathbf{75.0\text{ Ns/m}}$$

---

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
