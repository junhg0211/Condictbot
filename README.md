# Tobcidnock

> Conlangs for Discord

## Usage

[You can invite **Tobcidnock** to your server.](https://discordapp.com/api/oauth2/authorize?client_id=697316460237946890&permissions=0&scope=bot)

### Help

* You can use `@@help` to see list of commands.
* Also, you can use `@@help <command>` to see details on the command.

### Default Language Settings

* **Tobcidnock** can be used in 3 languages: Korean, English, and Japanese.
* With `@@setting language korean`, you can use **Tobcidnock** in Korean.
* With `@@setting language english`, you can use **Tobcidnock** in English.
* With `@@setting language japanese`, you can use **Tobcidnock** in Japanese.
* English and Japanese translation may not be perfect.
If you found an error in translation, please contact to links below or `@@contact` command.

### Create New Dictionary

* You can create a dictionary with its own name.
For example, command `@@dict create etten` makes new dictionary, *etten*.
* After a confirmation, you will be able to use your new dictionary.
* You can add the words with meanings in dictionary.

### Define a Word

* You can define a word with meaning.
* You will have to follow these steps:

1. `@@word dictionary <name>` to select your working dictionary.
2. `@@word define <word> <meaning>` to define your word.
You can use double quotation mark(`"`) to contain spaces in the word.
Meaning does not need quotation marks.

* If you want to change the meaning of a word,
simply do the same thing that what you did when you newly define a word.

### Search for a Word

* Defined word can be found through its word or meaning.
* If you want to search word `ettian` in `etten` dictionary,
you will have to follow these steps.

1. `@@word dictionary etten` to select your working dictionary to *etten*.
2. `@@word meaning ettian` to search meaning of *ettian*.
3. You also can search it with command `@@word ettian`.
(This method will not be able to search word 'meaning'.)
4. Simply `@?ettian` will do the same thing.

### Delete a Word

* You can delete words from dictionary.
* You will have to follow these steps:

1. `@@word dictionary <name>` to select your working dictionary.
2. `@@word delete <word>` to delete your word.
3. You also can delete a word with `define` keyword.
Define a word without meanings. Like `@@word define ettian`.

* Deleted word cannot be reloaded.
And also, deletion does not have reconfirmation procedure.
Be sure you want to delete a word when you use this command.

### Remove a Dictionary

* If you created a dictionary but it has no meaning at all,
you can remove a dictionary.
* You can remove a dictionary with `@@dict remove <name>`.
* After a confirmation, the dictionary will be removed.

### Contact

* If there is an error in transition or its feature,
please let me know and fix it.
* You can contact with:
  * Email  [junhg0211@gmail.com](mailto://junhg0211@gmail.com)
  * Twitter  [@YtScratch](https://twitter.com/YtScratch)
  * GitHub  [junhg0211](https://github.com/junhg0211)
  * Discord  스치#8861
