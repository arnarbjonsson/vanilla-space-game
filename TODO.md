# TODO List

## Priority Tasks
- [ ] 

## Features to Implement
- [ ] Create more module types for the spaceship (e.g., shield, boost, repair drone)
- [ ] Visual effects for laser impact on asteroids (particles, sparks, etc.)
- [ ] **Inventory UI**
  - [ ] Inventory panel in the top-right corner of the screen
    - [ ] Initially, display the text "Empty" if the inventory has no items
    - [ ] When items are present, display one line for each type in the inventory
        - [ ] Each line should show: [icon] quantity X name (e.g., [icon] 12 x Veldspar)
    - [ ] The UI should respond to inventory changes and update in real time
    - [ ] Style the panel for clarity and readability
- [ ] **Critical Hit Mining System**
  - [x] Add critical hit chance to mining laser module
  - [x] Implement variable mining outcomes (normal, critical, super-critical)
  - [x] Add visual feedback for critical hits (text colors)
  - [x] Balance mining rates and critical hit probabilities
  - [ ] Add sound effects for different mining outcomes
- [ ] **Dynamic Audio System with Pyo**
  - [ ] Integrate pyo audio library for procedural sound generation
  - [ ] Create unique sound profiles for each ore type
  - [ ] Implement dynamic frequency modulation based on amount mined
  - [ ] Add amplitude modulation based on mining success/critical hits
  - [ ] Create smooth transitions between different mining states
  - [ ] Add audio feedback for asteroid depletion

## Bugs to Fix
- [ ] 

## Improvements
- [x] **Mining Laser Visual Effect** - COMPLETED ✅
  - [x] Created effects renderer with registration system
  - [x] Added orange laser beam rendering between ship and asteroid
  - [x] Integrated effects renderer into main rendering pipeline
  - [x] Implemented clean registration/unregistration architecture
- [ ] 

## Documentation
- [ ] Update README.md with new module system controls

## Testing
- [ ] Test mining laser visual effects in-game
- [ ] 