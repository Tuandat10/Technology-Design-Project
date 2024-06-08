# Short Introduction
This project is created to meet the Technological Design Project Unit in Sem 1 2024. Our project group has four members, with Ha Trang Nguyen is a team leader. The project is how to create the food web application focusing on the logic to generate routing from places to places. 
# How to deploy the code
## The environment need to be deployed
1. Folium (pip install folium)
2. Geopy (pip install Geopy)
3. Openrouteservice (pip install openrouteservice)

## Step by step to deploy code
1. Open the folder droneproject in Technology-Design-Project in Visual Studio Code
2. Open Terminal
3. Run the command: python manage.py runserver

# Before run the code there is a big big mark that we want to say that since this is the prototype so there are limitations, and one of it is that when Customer start to order the food they need to finish a whole process, which means all the code below must be done from the very start at the very end since at the end of the code we have the syntax session.clear, so if the customer do not finish their journey to reach this code, further testing will get errors. Therefore, if the tutor get errors when deploying code because of forgetting to finish all the journey, they need to folk the code from github again to avoid errors.
### Customer side
1. Access the Customer UI by this url: localhost:8000. The user will access to the login page. At this stage the user can create a new account or you the existing one that team has created before (username: trangeupadi123@gmail.com password: 123123)
2. After login, user will access home page, at this stage, the user can click the food they want, or they can click to restaurant and choose food from restaurant page. At this stage we recommend the tutor to choose food from taco restaurant since in the restaurant side we will provide you an account of taco restaurant. PAY ATTENTION because of project's limitation so the user just only choose food from one restaurant each order otherwise, the user will get error in further steps.
3. After choosing all food, user can click to the basket on the top right of the screen, and user will access to the Cart page, and at this stage user just need to confirm and click next to further steps.
4. At the final step, when user click to track order, user will access to track page. Because all the logic is in this page so in further steps when the restaurant update any status of the order, we need to refresh the page so the logic will be run. PAY ATTENTION the user must need to click refresh (f5) instead of enter the url again because it will cause errors.

### Restaurant side
1. Access the the Restaurant UI by this url: http://localhost:8000/rsignin/ . The user will access to the login page. At this stage the user can create a new account but we do not recommend this, instead using this account to sign in: username: taco@gmail.com, password: 123456
2. After login, user will access dashboard restaurant page, and we just need to focus on the bar in the middle top of the page including 5 sections: New Order, Preparing, Ready, Delivering, Tracking order. After finish step 3 in Customer side, the New Order section in Restaurant UI will appear (changing from 0 to 1).
3. Restaurant user should go to each section and click the button in each section. But remember after clicking button in each section, tutor need to get back to track order page in customer side (do not close the track page since if the user close it, they cannot access the track page anymore but need to create a new order) and click refresh (f5) so the code in this page can run and it will update the tracking progress in Customer UI.
4. In Ready section, when Restaurant user go to this section, the path in Customer UI will change the route from restaurant to customer delivery address.
5. There is Tracking order section that helps Restaurant user track all the orders they get from customers.

### Admin side
1. Access the Admin UI by this url: http://localhost:8000/adminsignin/ . The user will access to the admin login page. At this stage, the user just only have an option to sign in by this account: username: admin, password: admin123
2. After loging, Admin user will access to admindashboard page, and in this page, admin can observer every drone on their way to destinations, admin have a permission to cancel any drone and make them to go to the charge station immediately.

 