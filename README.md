# ⏱️ WaitTime – Utilizing Waiting Time in Half-Duplex Communication

<p align="center">
  <b>Turning communication waiting time into useful local computation</b>
</p>

---

## 📌 Overview

**WaitTime** is a Computer Networks project that explores how the waiting time
that occurs during **half-duplex TCP communication** can be utilized for
performing useful local computations.

In conventional communication systems, the time spent waiting for a response
or for the communication turn may remain unused. This project measures that
waiting time and identifies how much of it can be effectively utilized for
local processing.

The system measures communication waiting time, computation time, utilized
waiting time, and unused waiting time, and presents the results through an
interactive dashboard.

---

## 🎯 Objectives

- Measure the waiting time during TCP communication.
- Measure the execution time of local computational tasks.
- Identify the portion of waiting time that can be utilized.
- Calculate utilized and unused waiting time.
- Visualize the experimental results through a dashboard.
- Demonstrate the potential of using communication waiting periods for
  useful computation.

---

## ⚙️ How It Works

```text
        ┌───────────────────────┐
        │   Start Communication │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │  Half-Duplex TCP      │
        │    Communication      │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Measure Waiting Time  │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Perform Local         │
        │ Computation           │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Calculate Utilized &  │
        │ Unused Waiting Time   │
        └───────────┬───────────┘
                    ↓
        ┌───────────────────────┐
        │ Streamlit Dashboard   │
        └───────────────────────┘
Uniuesness of our project:Utilizing the wait time
