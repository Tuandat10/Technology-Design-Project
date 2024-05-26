How can our project work
Our project is using drone to diliver food from restaurant to customer address.
At first, you will need to clone source code from github to your local machine. Then open the visual studio code, and drag the folder technology-design-project to visual studio code. Then open Terminal and cd droneproject.
At that time, you are standing at droneproject. run the command: python manage.py runserver. After you run server, access this url: http://localhost:8000/
After that, you will create your account (or we can use the default account: trangeupadi123@gmail.com with the password is 123123). After you create your account, your information will be saved in the database
After that, you will access the home page, you can walk around and see what our page can do
Main function:
For prototype, we will use: customer_username: trangeupadi123@gmail.com, password: 123123, restaurant_username: taco@gmail.com, password: 123456
In each food, you will see the plus icon, click to them to choose a food. REMEMBER THE CONSTRAINT OF OUR PROJECT IS WE JUST CHOOSE THE FOOD FROM ONE CUSTOMER PER ORDER (idealy, choose food from taco). So you should go to restaurant to choose the food.
After you finish choosing food, click to cart, to go to further steps
After you finish in payment success, click to track order, to view the map. The map will update based on the restaurant side. REMEMBER YOU MUST ONLY CLICK REFRESH OR F5 TO UPDATE THE MAP, DO NOT CLICK TO THE URL AND PRESS ENTER SINCE THE MAP PAGE IS SHOWING 
THANKS TO THE FORM SEND IN PAYMENT SUCCESS
Moving to restaurant sites, you must choose sign in to the restaurant you have order (taco). Then after you click confirm the order to ready, you can move to the map page in customer side and press refresh or f5 to see the update of the map. Then click to delivering
the map will update. And after you click delivered in restaurant side, the map page in customer side will updated to successfully ordered. 
SOME LOGIC IN THIS PROJECT:
1. when customer successfully order, the system will find the nearest charging station of restaurant, and then it will find the available drone in this charging station (the drone which has the highest battery), if there is no drone in the nearest station, it will
change the station, to find suitable drones.
2. After the restaurant make the food ready to deliver, the drone will head to the restaurant, and in the customer side, the map will be updated (the process and the flight path)
3. After the food is delivered, the drone will find the nearest charging location and check whether this charging station has available slot, if there is no any slot, it will find the second - nearest charging station and check whether these charging station has available slot, and it will repeat after drone find the suitable one
4. The maximum weight of food that one drone can take is 10 kg. If the weight of food is between 10 and 20, there are two drones will take the food. If the weight of food is larger than 20, the error will show.
5. The drone uses 1% of their battery for 2 km they travel.
6. After the drone finish delivering, and finding the charging station, the battery will be charge to be 100 again.
