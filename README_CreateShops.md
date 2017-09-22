# Create Shops PE
CreateShops PE is based off the original [CreateShops](https://www.youtube.com/watch?v=dMDnbyFDvXQ) filter by [SethBling](https://www.youtube.com/channel/UC8aG3LDTDwNR1UQhSn9uVrw)

Modified and updated by [Pathway Studios](http://pathway.studio) for PE 1.0+  
Follow us [@pathwaymc](https://twitter.com/@pathwaymc) on Twitter

# Screenshots
Trades Screen  
![Trade Screen](https://user-images.githubusercontent.com/1608235/29000334-5e3f89ae-7a35-11e7-9420-ffa3a1fee980.png "Trade Screen")

Help Screen  
![Help Screen](https://user-images.githubusercontent.com/1608235/29000335-6010e8ea-7a35-11e7-9363-dc0bc0a36624.png "Help Screen")

# How to use

## Chest Setup
To prepare a chest to be converted into a villager, you'll need to place the items in a specific format.

* The first row of the chest is BuyA
* The second row of the chest is BuyB (this is optional)
* The third row of the chest is Sell

Each column represents a different trade. 

In the following example the chest is setup to give the villager two trades.

* (1) Emerald + (1) Quartz gives (16) Bread
* (5) Emerald + (1) Enchanted Book gives (1) Enchanted Sword

![Chest Setup Example](https://user-images.githubusercontent.com/1608235/29000338-6a49d72c-7a35-11e7-97cc-257aff4e970f.png "Chest Setup Example")

## Custom Name & Custom Name Visible
This will set each villager created within the selection to this name and make it visible when a player looks at the villager.

This will **not** always display the villagers name; you'll need to modify your behavior pack in order to do that.

*Please note: This applies to **every** villager created within your selection. That means if you add the name Sally and select multiple chests, all resulting villagers will be named Sally*

## Reward XP
This is the amount of XP given for each trade a player makes.

## Professions
Though the Professions menu has multiple options, it really has two modes: Detect wool or set a specific profession. 

If you select a specific profession, **ALL** chests within your selection will turn into a villager using the profession you specified.

If you select Detect Wool, only chests with one of the following wool types placed directly above it will be converted into its associated villager profession.

* White -> Farmer
* Orange -> Fisherman
* Magenta -> Shepherd
* Light Blue -> Fletcher 
* Yellow -> Librarian
* Lime -> Cartographer
* Pink -> Cleric
* Gray -> Armorer
* Light Gray -> Weapon Smith
* Cyan -> Tool Smith
* Purple -> Butcher
* Blue -> Leather Worker

## Stop Trade Upgrade
This makes it so the villager's trade tier won't be upgraded and start adding trades from the respective villager's trade loot table. This sets the TradeTier to -2000000000, meaning a player would have to make 2 billion trades (most villagers 2 billion +1) before they pull from their loot tables. This means realistically, loot tables for the applicable villager or villager variant will not affect villagers created by this filter.

Alternatively, you could set the villager's (or villager variant's) loot table to an empty file within your behavior packs if you want more control.

## Max Health
This sets the health of a villager to 1024. If you want to make sure your villager can't be killed, setup a damage\_sensor in their behvaior pack to negate the type of damage you want to protect them from.

## Unlimited Trades
This makes your trades unlimited (effectively at least — it's about 2 billion trades).
