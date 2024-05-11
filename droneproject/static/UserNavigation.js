// Log in 
document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    if (loginButton) {
        loginButton.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = 'Home.html';
        });
    }
});



// Sign up for new account
document.addEventListener('DOMContentLoaded', function() {
    const signupLink = document.getElementById('signupLink');
    if (signupLink) {
        signupLink.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = 'Signup-(U).html';
        });
    }
});



// Sign in (redirect from sign up page)
document.addEventListener('DOMContentLoaded', function() {
    const signinButton = document.querySelector('.signinLink');
    if (signinButton) {
        signinButton.addEventListener('click', function(event) {
            event.preventDefault(); 
            window.location.href = 'Login-(U).html';
        });
    }
});



// Navigate to Restaurants.html
function navToResto() {
    window.location.href = '/Restaurants';
}
document.addEventListener('DOMContentLoaded', function() {
    const orderNowButton = document.getElementById('orderNow'); // Order Now button
    if (orderNowButton) {
        orderNowButton.addEventListener('click', function(event) {
            event.preventDefault();  // Prevent the default form submission
            window.location.href = '/Restaurants/';  // Correct path
    });

    const allFoodButton = document.getElementById('allFood'); // Categories - All food button
    if (allFoodButton) {
        allFoodButton.addEventListener('click', navToResto);}
    }
});

// Navigate to Track Order
document.addEventListener('DOMContentLoaded', function () {
    var trackOrderButton = document.querySelector('.track-order-button');
    if (trackOrderButton) {
        trackOrderButton.addEventListener('click', function () {
            window.location.href = 'Delivery.html';
        });
    }
});  



// Tracking Map
document.addEventListener('DOMContentLoaded', function () {
    // Create map and sets center (Melbourne, Hawthorn) and zoom level
    var map = L.map('map').setView([-37.8216, 145.0379], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var droneIcon = L.icon({
        iconUrl: 'img/track.png',
        iconSize: [52, 52],
        iconAnchor: [26, 26]
    });

    // Drone (starting point)
    var droneMarker = L.marker([-37.8216, 145.0379], { icon: droneIcon }).addTo(map);
    droneMarker.bindPopup("<b>Hello!</b><br>This is a drone delivery.").openPopup();

    // Destination
    L.marker([-37.8276, 145.0577]).addTo(map);

    // Define coordinates
    var deliveryPathCoordinates = [
        [-37.8216, 145.0379], 
        [-37.8276, 145.0577]  
    ];
    // Create a delivery path (route) using coordinates
    var deliveryPath = L.polyline(deliveryPathCoordinates, { color: '#FF5733' }).addTo(map);
    // Fit the map view to show all markers and path
    var bounds = L.latLngBounds([droneMarker.getLatLng(), deliveryPath.getLatLngs()]);
    map.fitBounds(bounds);
});



// Choose restaurant
document.addEventListener('DOMContentLoaded', function() {
    const restaurantItems = document.querySelectorAll('.restaurant-item');
    restaurantItems.forEach(function(restaurantItem) {
        restaurantItem.addEventListener('click', function() {
            const restaurantId = restaurantItem.id;

            let destinationUrl = '';
            switch (restaurantId) {
                case 'Resto2':
                    destinationUrl = "{% url 'Menu' %}"; // Menu page for Taco Bell
                    break;
                default:
                    break;
            }
            if (destinationUrl) {
                window.location.href = destinationUrl;
            }
        });
    });

    const suggestItems = document.querySelectorAll('.suggest-item');
    suggestItems.forEach(function(suggestItem) {
        suggestItem.addEventListener('click', function() {
            const suggestId = suggestItem.id;

            let destinationUrl = '';
            switch (suggestId) {
                case 'Suggest1':
                    destinationUrl = suggestItem.getAttribute('data-url');
                    if (destinationUrl) {
                        window.location.href = destinationUrl;
                    }
                    break;
                case 'Suggest2':
                    destinationUrl = ''; // Menu page for Suggested Restaurant 2
                    break;
                default:
                    break;
            }
            if (destinationUrl) {
                window.location.href = destinationUrl;
            }
        });
    });
});

// Navigate between the steps (in cart page)
document.addEventListener('DOMContentLoaded', function() {
    const stepContainers = document.querySelectorAll('.step-container');
    stepContainers.forEach(function(stepContainer, index) {
        stepContainer.addEventListener('click', function() {
            let targetPage = '';
            switch (index) {
                case 0:
                    targetPage = 'Cart.html';
                    break;
                case 1:
                    targetPage = 'Shopping-Info.html';
                    break;
                case 2:
                    targetPage = 'Address.html';
                    break;
                case 3:
                    targetPage = 'Payment-no-card.html';
                    break;
                default:
                    break;
            }
            if (targetPage) {
                window.location.href = targetPage;
            }
        });
    });
});



// Add item to cart
document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.querySelector('.menu-add-btn');
    if (addButton) {
        const itemName = document.querySelector('.font-semibold').innerText;
        const itemPrice = parseFloat(document.querySelector('.text-xl').innerText.slice(1));
        addButton.addEventListener('click', function(event) {
            event.preventDefault();
            addToCart(itemName, itemPrice); // Add item
        });
    }
});

function addToCart(itemName, itemPrice) {
    const cartItems = getCartItems();
    const existingItem = cartItems.find(item => item.name === itemName);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cartItems.push({ name: itemName, price: itemPrice, quantity: 1 });
    }
    updateCartItems(cartItems); // Update database
}

function getCartItems() {
    return JSON.parse(localStorage.getItem('cartItems')) || [];
}

function updateCartItems(cartItems) {
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
}



// Navigate to next page based on current page
document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('.next-button');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const currentPage = getCurrentPage(); 
            const nextPage = getNextPage(currentPage);
            if (nextPage) {
                // Get the URLs from the data attribute
                const urls = JSON.parse(document.body.getAttribute('data-urls'));
                // Navigate to the next page
                window.location.href = urls[nextPage];
            }
        });
    }
});


// Function to get current page name
function getCurrentPage() {
    const currentPageUrl = window.location.href; // Extract current page from URL
    const currentPageName = currentPageUrl.substring(currentPageUrl.lastIndexOf('/') + 1).split('.')[0];
    return currentPageName;
}

// Function to determine the next page based on current page
function getNextPage(currentPage) {
    const pageMap = { // Define a mapping
        'Cart': 'Shopping-Info',
        'Shopping-Info': 'Address',
        'Address': 'Payment-no-card',
        'Payment-no-card': 'Payment-success'
    };
    return pageMap[currentPage];
}



// Add new address
document.addEventListener('DOMContentLoaded', function() {
    const addAddressButton = document.querySelector('.add-address-button');
    if (addAddressButton) {
        addAddressButton.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = 'Add-address.html';
        }); 
    }
});



// Add new card
document.addEventListener('DOMContentLoaded', function() {
    const addCardButton = document.querySelector('.add-card-button');

    if (addCardButton) {
        addCardButton.addEventListener('click', function() {
            window.location.href = 'Add-card.html';
        });
    }
});



// Save button
document.addEventListener('DOMContentLoaded', function() {
    const saveButton = document.querySelector('.save-button');
    if (saveButton) {
        saveButton.addEventListener('click', function(event) {
            event.preventDefault();
            const currentPage = getCurrentPageName();
            if (currentPage === 'Add-card') {
                window.location.href = 'Payment-have-card.html';
            } else if (currentPage === 'Add-address') {
                window.location.href = 'Address.html';
            }
        });
    }
});

function getCurrentPageName() {
    const currentPageUrl = window.location.href;
    const currentPageName = currentPageUrl.substring(currentPageUrl.lastIndexOf('/') + 1).split('.')[0];
    return currentPageName;
}



// Close add-card tab
document.addEventListener('DOMContentLoaded', function() {
    const closeButton = document.querySelector('.close-button');

    if (closeButton) {
        closeButton.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.href = 'Payment-no-card.html';
        });
    }
});



// Pay the order
document.addEventListener('DOMContentLoaded', function() {
    const payConfirmButton = document.querySelector('.pay-button');

    if (payConfirmButton) {
        payConfirmButton.addEventListener('click', function() {
            window.location.href = 'Payment-success.html';
        });
    }
});


document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready');
    const sidebarButtons = document.querySelectorAll('.sidebar-button');
    sidebarButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const destinationUrl = button.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
});
//     function getPageFromButtonText(buttonText) { // Determine destination
//         const pageMap = {
//             'Personal Info': '/Profile/',
//             'My address': '/My-address/',
//             'Favorite': '/Favourite/',
//             'Order History': '/My-order-history/',
//             'Notifications': '/Notification/',
//             'Payment Method': '/Payment/',
//             'Settings': '/Settings/',
//             'Log Out': '/Logout/'
//         };
//         return pageMap[buttonText];
//     }
// });