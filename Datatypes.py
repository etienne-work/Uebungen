# dict
people = {
    "Etienne": {
        "name": "Mannhart",
        "age": 19,
        "lieblingsbuchstabe": bytearray("E", "UTF-8"),  # byteArray -> für memview
        "toDoListe": ["planen"],  # list
        "salatkombo": (
            "Frenchdressing",
            "Blatt",
            "Gruyer",
        ),  # tuple (unchangeable) -> convert to list add value -> convert to tuple
        "früchte": {"Apfel", "Banane"},  # set -> add or remove values
    },
    "Max": {
        "name": "Muster",
        "age": 21,
        "lieblingsbuchstabe": bytearray("M", "UTF-8"),  # byteArray -> für memview
        "toDoListe": ["singen"],  # list
        "salatkombo": ("Frenchdressing", "Blatt", "Tomate"),  # tuple
        "früchte": {"Apfel", "Kirsche"},  # set
    },
}

name = input("gesuchten Vornamen eingeben: ")
# lowercase all then capitalize first letter.
# z.B. name = "etIenne" wird akzeptiert (-> umwandlung in Etienne)
name = name.lower().capitalize()


# überprüfe ob Namen in Dictionary
def test() -> bool:
    if name not in people.keys():
        print(f"Kein person mit Vorname {name}")
        return False
    return True


# modifikationsbeispiele der Arrays
def modify() -> None:
    # modifikation liste
    people[name]["toDoListe"].append("programmieren")

    # modifikation tuple (an sich nicht veränderbar)
    tempList = list(people[name]["salatkombo"])
    tempList.append("Gruyer")  # tuple ist indexiert (erlaubt duplicates)
    people[name]["salatkombo"] = tuple(tempList)

    # modifikation set (values nicht änderbar aber hinzufüg-/entfernbar)
    people[name]["früchte"].add("Orange")
    people[name]["früchte"].discard("Apfel")

    # modifikation Dictionary
    people["Fritz"] = {"name": "Muster", "age": 21}
    people.update({"Jonas": {"name": "Meier"}})


# output Values of dic (person) including keys
def __str__() -> str:
    formattedText = ""
    for person, item in people.items():
        formattedText += f"Vorname: {person}"
        for infoName, info in item.items():
            if infoName != "lieblingsbuchstabe":
                formattedText += f"\n{infoName}: {info}"
            else:  # Ausgabe Buchstabe als Buchstabe, Unicode & Memview
                formattedText += f"\n{infoName}: {chr(ord(info))}, Unicode: {info[0]}, Memview von byte-Array {bytes(info[0:1])}"
        formattedText += "\n\n"
    return formattedText


# run
if test():
    print("original version:")
    print(__str__())

    print("modified version:")
    modify()
    print(__str__())
