SLIME SURVIVAL 
===============	

--- v.0.x: basic gameplay ---
---------------

## v.0.4: player die
???

## v.0.3: player level up

### feat

- player's indexs
    + exp, level
    + healthy
    + atk
    + agility
    + def

- Player kill enemy
    + Deals damage to enemy
    + Receive exp when enemy die

- level up
    + level up --> increase exp to level up &  receive index

- add index
    + GUI add index
    + add index


## v.0.2: enemy movement & animation

### feat

- enemy: create --> follow --> attack --> die
    + create: has value exp
    + if around, follow player
    + if nearly, attack player
    + die
    + asset: sound: spawn, jump, attack, die

- Random monster spawn


## v.0.1: player movement & animation

### feat

- player animation: 4 directions top, down, left, right
    + Idle
    + Walk
    + Attack

- asset: sound walk, attack


## v.0.0: init - 10/09/2023

### feat
- Add map: center map (delta)

- Add sprite: player, slime

- Skeleton code:
    + Simple tile (map)
    + Player can move
    + Camera follow player