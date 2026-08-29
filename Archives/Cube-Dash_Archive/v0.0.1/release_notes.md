# Cube Dash v0.0.1-alpha

### 🚀 Initial Engine Core Deployment

This release marks the official deployment of the initial core architecture for **Cube Dash** (Development Codename: *Project Jettison*). The engine is written natively from scratch in pure C using Raylib, compiled with minimal zero-installer optimizations via the `w64devkit` toolchain.

***

### 📦 How to Download and Play

You do not need to install any software packages to run Cube Dash. It is distributed as a completely portable, standalone deployment.

1. Scroll down to the **Assets** section at the bottom of this release page.
2. Download the compressed file matching your computer's hardware profile:
   * Choose `cubedashwin64.zip` for modern 64-bit systems.
   * Choose `cubedashwin32.zip` for legacy 32-bit systems.
3. Locate the downloaded file in your downloads folder, right-click it, and select **Extract All...** to unpack the archive folder.
4. Open the extracted folder and double-click **cubedash-win32.exe`** or **`cubedash-win64.exe`** to boot the game engine instantly.

***

### 🎮 Implemented Systems & Mechanics

* **Rhythmic Physics Foundation:** Engineered a dedicated fixed-interval movement ticker featuring automated horizontal forward velocity, rigid gravity multipliers, and responsive vertical jump constraints.
* **Dual-Architecture Build Profiles:** Fully compiled and optimized standalone binary profiles supporting both modern 64-bit (`x86_64`) and legacy backwards-compatible 32-bit (`i686`) Windows hardware layers.
* **Modular Codebase Segmenting:** Organized codebase into decoupled source profiles (`main.c`, `player.c`, `obstacles.c`) to maintain a clean separation of concerns and high-performance execution.

***

### ⚙️ Compilation & Local Build Instructions

To build the project tree manually from source rather than using the pre-compiled binary zips attached below, run your automated workspace script inside your local project directory:

```bash
./build.bat
```

***

### 📜 Licensing Notice
This release stream is fully managed and legally protected under the **PolyForm Noncommercial License 1.0.0**. Educational forks, source inspection, and personal tinkering loops are permitted. Commercial distribution, optimization resale, or monetization is strictly prohibited.
