from sys import exit


def addon():
    response = input(
        """
        What else do you want to add?
        1. Soup
        2. Meat
        3. Fish
        4. Drink
        5. None

    >>>>"""
    )
    if response == 1 or response == "1":
        response = input(
            """
        1. Egusi
        2. Ewedu
        3. Ogbono
        4. Vegetable
        5. None
        
    >>>>"""
        )
    if response == 2 or response == "2":
        response = input(
            """
        1. Beef
        2. Chicken
        3. Turkey
        4. None
        
    >>>>"""
        )
    if response == 3 or response == "3":
        response = input(
            """
        1. Eja kika
        2. Smoked Titus
        4. None
        
    >>>>"""
        )
    if response == 4 or response == "4":
        response = input(
            """
        1. Sprite
        2. Pepsi
        3. Hollandia
        4. None
        
    >>>>"""
        )


if __name__ == "__main__":
    while True:
        response = input(
            """
        1. Snacks and Drinks
        2. Traditional dish
        
    >>>>"""
        )
        if response == 1 or response == "1":
            response1 = input(
                """
            1. Puff puff
            2. Fish roll
            3. egg roll
            4. None
            
        >>>>"""
            )
            if response1 != 4 or response1 != "4":
                addon()
            response1 = input(
                """
                Do you want anything else?
                1. Yes
                2. No
            """
            )
            while response1 == 1 or response1 == "1":
                addon()
                response1 = input(
                    """
                Do you want anything else?
                1. Yes
                2. No
            """
                )
            continue

        if response == 2 or response == "2":
            response2 = input(
                """
            1. Jollof rice
            2. Fried rice
            3. Yam and egg
            4. None
            
        >>>>"""
            )
            if response2 != 4 or response2 != "4":
                addon()
            response2 = input(
                """
                Do you want anything else?
                1. Yes
                2. No
            """
            )
            while response2 == 1 or response2 == "1":
                addon()
                response2 = input(
                    """
                Do you want anything else?
                1. Yes
                2. No
            """
                )
            continue
