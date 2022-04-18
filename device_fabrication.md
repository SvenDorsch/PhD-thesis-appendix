# Device-fabrication
In this document process steps and parameters for the fabrication of nanowire based quantum dot devices are given. A detailed discussion of the various different device designs including advantages, disadvantages and applications as well as scanning electron microscope images of finished devices can be found in in section 5 and 6 of the thesis.

Note that all fabrication steps are based on pre-patterned silicon substrates with a degenerate n-doped and metallized backgate. The device chips contain 10 100x100 micrometer write fields with coordinate markers. Each write-field has access to 12 bond pads. 
Before any further processing can occur, the chips are cleaned in acetone and 2-propanol for three minutes each with ultrasonic agitation followed by drying under N<sub>2</sub> flow.

This document organizes as follows:
1. [Fabrication of combined bottom-gate and heater arrays](#Bottom-gates)
2. [Contacting of nanowires including side-gate and heater electrodes](#Nanowire-contacts)
3. [Fabrication of top-heater structures](#Top-heaters)

## Bottom-gates
The bottom-gate design employed for devices discussed here consists of 50nm wide, 10nm high and 50nm spaced gate stripes. Several gate arrays are deposited in each write field. Selected gates can be contacted on both ends and double function as local Joule-heater electrodes.

1. Spin coating: ARP6200.04 EBL resist:
    - Prepare substrate: O<sub>2</sub> plasma ashing (Plasma preen), 60s followed by a pre-bake for 60s at 150°C (hotplate). Note that this is necessary for good adhesion of the ARP resist to the substrate surface.
    - Spin coater: ARP6200.04 resist, 6000rpm, 60s
    - Post-bake: 60s at 150°C (hotplate)
2. EBL exposure of the bottom-gate pattern:
    - EBL-Raith150: 30kV acceleration voltage, 10µm aperture. Use three-point focus and several alignment steps per write field.
3. Development: 
    -  60s amyl acetate, little to no stirring to avoid damaging the gate structures
    -  15s 2-propanol, little to no stirring
    -  dry under N<sub>2</sub> flow
    -  O<sub>2</sub> plasma ashinng, 12s
4. Metallization: Thermal evaporation in AVAC or Temescal.
    - 2nm Ti and 8nm Ni
5. Lift-off: 
    - Remover 1165 at 90°C, 10 minutes
    - Apply ultrasonic agitation, 60s
    - Remover 1165 at 90°C, 5 minites
    - Apply ultrasonic agitation, 60s
    - 2-propanol rinse
    - dry under N<sub>2</sub> flow
6. Spin coating: PMMA 950A5 EBL resist for high-k window
    - Spin coater: PMMA 950A5 resist, 5000rpm, 60s
    - Post-bake: 3 minutes at 180°C (hotplate)
7. EBL exposure of high-k window:
    - EBL-Raith150: 20kV acceleration voltage, 20µm aperture, single focus point and one alignment step per write field sufficient
8. Development:
    - MIBK:IPA = 1:3, 45s
    - 2-propanol, 20s
    - dry under N<sub>2</sub> flow
    - O<sub>2</sub> plasma ashing: 30s
9. Oxide deposition: HfO<sub>2</sub>:
    - ALD-Savannah: 80 cycles HfO<sub>2</sub>
10. ALD lift-off. Note that this lift-off is difficult and works best when left in acetone overnight. If initial lift-off as described here does not succed, a heated remover 1165 lift-off process is recommended.
    - Acetone and ultrasonic agitation, 5 minutes, maximum power
    - Submerge in acetone/2-propanol mix overnight
    - Apply ultrasonic agitation, 5 minutes, maximum power
    - 2-propanol rinse
    - dry under N<sub>2</sub> flow
11. Plasma ashing to remove residual resist:
    - O<sub>2</sub> plasma ashing, 30s
12. Nanowire deposition:
    - use a micromanipulator to deposit nanowires on top of the gate arrays.

## Nanowire-contacts
This is the most general process step, where Ni/Au contacts are fabricated to contact pre-deposited nanowires. In the same step, side-gates or side-heaters can also be fabricated. Accorate nanowire locations are found by imaging random deposited nanowires and identifying their position relative to the coordinate grid in the write fields.

1. Spin coating: PMMA 950A5 EBL resist for high-k window
    - Spin coater: PMMA 950A5 resist, 5000rpm, 60s
    - Post-bake: 3 minutes at 180°C (hotplate)
2. EBL exposure of high-k window:
    - EBL-Raith150: 20kV acceleration voltage, 20µm aperture for structures larger than 100nm, single focus point sufficient
    - EBL-Raith150: 30kV acceleration voltage, 10µm aperture for structures smaller than 100nm, use three-point focus
    - If accurate placement of structures with errors less than 100nm required: Several alignment steps per write-field recommended.
3. Development:
    - MIBK:IPA = 1:3, 45s
    - 2-propanol, 20s
    - dry under N<sub>2</sub> flow
    - O<sub>2</sub> plasma ashing: 12s if 30kV exposure or 20s if 20kV exposure
4. Nanowire oxide etch: Note that this step is critical to achieve good electrical contact to the semiconductor nanowires. Chemicals and etch times vary for different nanowire materials, doping, thickness etc. and the values given here only work with certainty for the specific nanowires used in the thesis. It is further critical to metallize the contacts immediately after the oxide removal to avoid reoxidation of the nanowire surface.
    - InAs nanowires: Sulphur passivation. See https://doi.org/10.1088/0957-4484/18/10/105307 for details.
        - Heat DI water to 40°C, stir with magnetic rotor
        - Submerge glass tube with 5% NH<sub>4</sub>S<sub>x</sub> solution in heated DI water
        - Submerge sample for 120s in 5% NH<sub>4</sub>S<sub>x</sub> solution
        - H<sub>2</sub>O rinse
        - Dry under N<sub>2</sub> flow
    - GaSb nanowires: HCl:2-propanol etch
        - 1.25M HCl - 2-propanol etchant solution, 35s
        - 2-propanol rinse
        - Dry under N<sub>2</sub> flow
    - InSb nanowires: 
        - 1.25M HCl - 2-propanol etchant solution, 60s
        - 2-propanol rinse
        - Dry under N<sub>2</sub> flow
5. Metallization: Thermal evaporation in AVAC or Temescal.
    - 25nm Ni and 75nm Au
6. Lift-off. Note that ultrasonic agitation will damage/remove the nanowires and can thus not be used in this process step.
    - Acetone, 60°C, 15 minutes
    - Use pipette to generate gentle acetone flow across substrate surface
    - Acetone, 60°C, 10 minutes
    - Use pipette to generate gentle acetone flow across substrate surface
    - 2-propanol rinse
    - dry under N<sub>2</sub> flow 
7. Plasma ashing to remove residual resist:
    - O<sub>2</sub> plasma ashing, 30s


## Top-heaters
This section describes the fabrication of top-heater electrodes on a device where a contacted nanowire is already present. As ultrasonic agitation can no longer be used to avoid damage to the nanowire, depositing the dielectric layer in a pre-defined high-k window is no longer a viable option. Thus, FIB milling is used to access underlying patterns.

1. Oxide deposition: HfO<sub>2</sub>:
    - ALD-Savannah: 80 cycles HfO<sub>2</sub>
2. FIB milling:
    - FIB-SEM: Mill through HfO<sub>2</sub> layer
3. Spin coating: PMMA 950A5 EBL resist for high-k window
    - Spin coater: PMMA 950A5 resist, 5000rpm, 60s
    - Post-bake: 3 minutes at 180°C (hotplate)
4. EBL exposure of high-k window:
    - EBL-Raith150: 20kV acceleration voltage, 20µm aperture for structures larger than 100nm, single focus point sufficient
    - EBL-Raith150: 30kV acceleration voltage, 10µm aperture for structures smaller than 100nm, use three-point focus
    - If accurate placement of structures with errors less than 100nm required: Several alignment steps per write-field recommended.
5. Development:
    - MIBK:IPA = 1:3, 45s
    - 2-propanol, 20s
    - dry under N<sub>2</sub> flow
    - O<sub>2</sub> plasma ashing: 12s if 30kV exposure or 20s if 20kV exposure
6. Lift-off. Note that ultrasonic agitation will damage/remove the nanowires and can thus not be used in this process step.
    - Acetone, 60°C, 15 minutes
    - Use pipette to generate gentle acetone flow across substrate surface
    - Acetone, 60°C, 10 minutes
    - Use pipette to generate gentle acetone flow across substrate surface
    - 2-propanol rinse
    - dry under N<sub>2</sub> flow 
7. Plasma ashing to remove residual resist:
    - O<sub>2</sub> plasma ashing, 30s
 
