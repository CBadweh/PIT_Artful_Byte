# CCS MSP430FR2355 LaunchPad – Flash / "Initializing target support" Fix

## What’s going on

- **Target config is correct:** MSP430FR2355, TI MSP430 USB1.
- **"Connected Targets" is empty** → CCS does not see the debug probe.
- **Device Manager** only shows generic **USB Serial Device (COM7/10)** and no **Texas Instruments** or **MSP430** device → Windows is not using TI’s debug driver for the eZ-FET.

The **MSP430FR2355 LaunchPad** uses an onboard **eZ-FET** (CDC-based). Both the **FET** and **CDC** drivers need to be installed so CCS can see the board.

---

## Step 1: Install the CDC driver (eZ-FET)

You already installed the FET driver. Install the **CDC** driver as well (required for eZ-FET):

1. **Close** Code Composer Studio.
2. Open **Command Prompt as Administrator** (Win → type `cmd` → right‑click **Command Prompt** → **Run as administrator**).
3. Run:

```bat
"C:\ti\ccs2041\ccs\ccs_base\emulation\drivers\msp430\DPInst\DPInst64.exe" /path "C:\ti\ccs2041\ccs\ccs_base\emulation\drivers\msp430\USB_CDC"
```

4. If the wizard asks to install or update, complete it.
5. **Unplug** the LaunchPad, wait ~10 seconds, **plug it back in**.

---

## Step 2: Check Device Manager again

1. Win + X → **Device Manager**.
2. With the LaunchPad connected, check:
   - **Ports (COM & LPT)** – COM7/COM10 are OK.
   - **Universal Serial Bus devices** – you want to see something like **Texas Instruments MSP430 USB** or **MSP430 eZ-FET** (no yellow warning).
   - **Other devices** – if anything has a yellow warning and looks like “MSP430” or “Texas Instruments”, that’s the probe; it needs the TI driver (Step 3).

If you still only see generic **USB Serial Device** and **USB Composite Device** and no TI/MSP430 entry, go to Step 3.

---

## Step 3: Manually bind the TI driver (if needed)

If the probe appears under **Other devices** with a yellow warning (or you see a generic “USB Serial Device” that you know is the LaunchPad):

1. In Device Manager, right‑click that device → **Update driver** → **Browse my computer for drivers**.
2. **Browse** to:
   `C:\ti\ccs2041\ccs\ccs_base\emulation\drivers\msp430\USB_CDC`
3. Check **Include subfolders**.
4. Click **Next** and let Windows install. If it says “best driver already installed”, try the **USB_FET** folder instead:
   `C:\ti\ccs2041\ccs\ccs_base\emulation\drivers\msp430\USB_FET_Win7_8_10_64`
5. Unplug and replug the LaunchPad.

**Success:** In Device Manager under **Ports (COM & LPT)** you should see **MSP Application UART1** and **MSP Debug Interface** (with COM numbers). No yellow warnings. Then go to Step 4.

---

## Step 4: Test in CCS

1. Open **Code Composer Studio**.
2. **View** → **Target Configurations** (or open the Target Configurations view).
3. **Test the connection:**
   - **CCS Theia (newer UI):** Right‑click your **.ccxml** → **Start Project-less Debug**. This tries to connect to the board without loading a project. If it connects, you’ll get a debug session; if it fails, you’ll see an error (that’s the “test”).
   - **Classic CCS (Eclipse-based):** Right‑click the .ccxml → **Test Connection** or **Launch Selected Configuration**.
   - If it says **connection successful** (or a debug session starts), try **Run** → **Debug** on your Blink LED project to flash.
   - If it fails, note the **exact error message** (e.g. “No probes found”, “Could not open port”).
4. If **TI MSP430 USB1** still fails, try **TI MSP430 USB2** or **USB3** in the .ccxml (Connection dropdown), save, and test again.

---

## If it hangs at “Initializing target support”

Drivers are OK (MSP Debug Interface in Device Manager) but the debug session never finishes. Try these in order:

1. **Slow down JTAG/SBW**
   - Open your **.ccxml** → **Advanced** tab.
   - Set **JTAG/SBW Speed** to **Slow** (instead of Medium or Fast). Save and try **Start Project-less Debug** again.

2. **Run CCS as Administrator**
   - Close CCS. Right‑click the CCS icon/shortcut → **Run as administrator**. Try **Start Project-less Debug** again.

3. **Use a different USB port**
   - Unplug the LaunchPad. Plug it into a **USB 2.0** port (not a blue USB 3.0 port if you have both). Wait for Windows to finish installing, then try again. Some PCs are flaky with USB 3.0 for debug probes.

4. **Nothing else using the debug port**
   - Close any serial terminal (PuTTY, Tera Term, etc.) that might have **COM7** (MSP Debug Interface) open. Close other CCS instances or TI tools (Uniflash, etc.). Unplug/replug the board, then try again.

5. **New target configuration**
   - **File** → **New** → **Target Configuration File**. Name it e.g. `MSP430FR2355_new.ccxml`, choose a location. In the wizard: **Connection** = **TI MSP430 USB1**, **Board or Device** = **MSP430FR2355**. Save. In your project, switch to this new config (or set it as default) and try **Start Project-less Debug** again. Sometimes the original .ccxml is in a bad state.

6. **Timeout (Advanced tab)**
   - In the .ccxml **Advanced** tab, look for any **Timeout** or **Connection timeout** option and increase it (e.g. to 30–60 seconds), then try again.

If it still hangs, report back: connection (USB1/2/3), JTAG/SBW speed, and whether you’re on USB 2.0 or 3.0.

---

## Step 5: Other checks

- Use a **USB 2.0 port** (not only USB 3.0).
- Try another **USB cable** (data-capable, not charge-only).
- Run **CCS as Administrator** (right‑click CCS → Run as administrator) and try flashing again.
- Ensure the **two boards** on the LaunchPad are **firmly connected** and in the **correct orientation**.

---

## If it still doesn’t work

Share:

1. What appears under **Universal Serial Bus devices** and **Other devices** in Device Manager (exact names, any yellow marks).
2. The **exact message** from **Test Connection** in CCS (or a screenshot).

Then we can target the next step (e.g. different driver path or connection type).

---

## Error: "spawn ./DSLite ENOENT"

**What it means:** The board shows in **Connected Targets**, but when you start debug/flash, CCS tries to run a program named `DSLite` and Windows can’t find it (ENOENT = file not found). CCS Theia’s debug path expects a `DSLite` executable that is **not** included in the Windows Theia install (only Linux-style or a different component has it).

**Fixes to try:**

### 1. Use Eclipse-based (classic) CCS instead of Theia

Your install may include both Theia and the older Eclipse-based CCS. The Eclipse version uses a different debug backend and does **not** rely on spawning `./DSLite`, so flashing usually works.

- Check the **Start Menu** or desktop for two shortcuts, e.g. **"Code Composer Studio"** (Theia) and **"Code Composer Studio (Eclipse)"** or **"CCS - Legacy"**. Launch the **Eclipse** one.
- Or run the Eclipse launcher by hand:
  - Open: `C:\ti\ccs2041\ccs\eclipse\`
  - Run **`ccs-server.exe`** (or the main CCS executable in that folder).
- In that IDE, open your project and the same target config (e.g. MSP430FR2355 / TI MSP430 USB1), then **Run → Debug** to flash.

### 2. Reinstall CCS with full / custom components

If you only have Theia and no Eclipse option:

- Run the CCS installer again. Choose **Custom** (or **Full**) installation.
- Ensure **all MSP430** components and **Debug Server** (or equivalent) options are selected so that the Windows debug server (and any DSLite-related files) are installed.
- After reinstall, try flashing again from Theia.

### 3. If you must use Theia on Windows

This error is a known limitation of the Theia + cloud-agent path on Windows. Until TI fixes it or provides a Windows DSLite binary in that path, the reliable workaround is to use **Eclipse-based CCS** (option 1) for flashing and debugging.

### 4. Workaround: Use MSP430Flasher command-line tool

If Eclipse CCS doesn't work, use MSP430Flasher (command-line) to flash:

1. Build your project in CCS Theia (Build works, only Debug is broken)
2. Convert `.out` to `.hex`:
   ```bash
   "C:\ti\msp430-gcc\bin\msp430-elf-objcopy.exe" -O ihex "path\to\Debug\project.out" "output.hex"
   ```
3. Flash with MSP430Flasher:
   ```bash
   "C:\ti\msp430ware_3_80_14_01\msp_flasher\MSP430Flasher.exe" -w "output.hex" -v
   ```

---

## Error: "Could not set device Vcc"

**What it means:** MSP430Flasher cannot control the target board's power supply.

**Fixes:**

1. **Check jumpers:** All 5 jumpers (VCC, TST, RST, RXD, TXD) must be installed on the LaunchPad
2. **Try a different USB port:** Use a USB 2.0 port directly on your PC (not a hub)
3. **Check USB cable:** Use a data-capable USB cable (not charge-only)
4. **Update FET firmware:** In CCS, right-click target config → "Update Firmware"
5. **Power issue:** The eZ-FET debugger might be faulty - try a different LaunchPad if available
6. **Use UniFlash GUI:** Download TI UniFlash (GUI tool) which handles power issues better than command-line MSP430Flasher
