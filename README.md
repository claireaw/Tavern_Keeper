<h1>Tavern Keeper: A Guide</h1>
<h2>Introduction</h2>
This is a quick guide to the operations of the Tavern Keeper Discord bot. This will cover how each of the commands work, and each of their use cases. Unless otherwise stated, all commands produce an emphemeral message, or one only visible to the user inputting the command.

<h2>/setup</h2>
This command sets up a user in the database. The user is prompted to enter a specific username. A user who already exists in the system but tries to register will recieve a message alerting them to the fact.

Users who abuse this can have their name altered or be removed from the system altogether.

<h2>/whoami</h2>
This command lists a user's username and currency amount. A user who does not exist will receive a message prompting them to run "/setup".

<h2>/helpme</h2>
This command publically lists all other commands that are available to users with any permissions. It does not list any commands that require a "staff" role.

<h2>/seestore</h2>
This command publicly displays the list of items available to purchase from the Astral Merchant, as well as their respective prices. This can currently be done by any user, regardless of store affiliation.

<h2>/seeitem</h2>
This command displays the qualities of a specific item. The user is prompted to enter a specific item name. The command shows the name, rarity, price, and respective Griffin's Saddlebag URL. This can currently be done by any user, regardless of store affiliation.

<h2>/buyitem</h2>
This command allows a user to "purchase" an item from the Astral Merchant store, removing it from the storefront and placing it in their inventory. The user is prompted to enter the name of the item they wish to purchase.

Currently, there is a slight bug, where a user who is not entered into the system will not recieve a response message if they they try to purchase an item. The correct behavior would be to prompt them to run "/setup".

<h2>/addpoint</h2>
THIS COMMAND ONLY WORKS FOR USERS WITH THE "STAFF" ROLE

This command allows a staff member to add a currency point to another specific user. The staff member is prompted for the user's username. The system will then add one point to that specified user.

<h2>/announce</h2>
THIS COMMAND ONLY WORKS FOR USERS WITH THE "STAFF" ROLE

This command allows a staff member to announce a change in the Astral Merchant's stock. It publically prints the message: "The Astral Merchant has been updated!".

<h2>TODO</h2>
   * <s>Fix bug related to purchasing items</s>
   * <s>Clean up output to be more human-readable</s>
   * <s>Ensure close to 100% uptime for project</s>
   * Improve purchasing method to discourage nested statements
   * Add refusal messages to a non-permissioned user requesting a permissioned command. Currently it just fails.
   * Switch out messy logic with comparative statements.
   ----------------------------------------------------------------------------------------------------------------------------------------------------------
   <h1>Commands exclusive to Tavern Keeper 2</h1>
   <h2>/resetshop</h2>
   THIS COMMAND ONLY WORKS FOR USERS WITH THE "STAFF" ROLE

   This commands allows a staff member to reset the contents of the shop. The staff member is prompted for an extra input to ensure this command is not run accidentally.
