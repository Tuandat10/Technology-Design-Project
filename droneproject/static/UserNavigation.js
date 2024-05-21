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
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const trackOrder = document.querySelectorAll('.track-order-button');
    trackOrder.forEach(function(trackOrder, index) {
        trackOrder.addEventListener('click', function() {
            const destinationUrl = trackOrder.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
});
// document.addEventListener('DOMContentLoaded', function () {
//     var trackOrderButton = document.querySelector('.track-order-button');
//     if (trackOrderButton) {
//         trackOrderButton.addEventListener('click', function () {
//             window.location.href = 'Delivery.html';
//         });
//     }
// });  



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
    console.log('Document is button');
    const stepContainers = document.querySelectorAll('.step-container');
    stepContainers.forEach(function(stepContainer, index) {
        stepContainer.addEventListener('click', function() {
            const destinationUrl = stepContainer.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const nextButton = document.querySelectorAll('.next-button');
    nextButton.forEach(function(nextButton, index) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
});


// Add item to cart
document.addEventListener('DOMContentLoaded', function() {
    const addButtons = document.querySelectorAll('.menu-add-btn');
    addButtons.forEach(function(addButton) {
        addButton.addEventListener('click', function(event) {
            event.preventDefault();
            const parentElement = addButton.closest('.parent-class');
            console.log(parentElement);
            const itemName = parentElement.querySelector('.font-semibold').innerText;
            const itemPrice = parseFloat(parentElement.querySelector('.text-xl').innerText.slice(1));
            addToCart(itemName, itemPrice); // Add item
        });
    });
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
    console.log('Document is button');
    const addAddress = document.querySelectorAll('.add-address-button');
    addAddress.forEach(function(addAddress, index) {
        addAddress.addEventListener('click', function() {
            const destinationUrl = addAddress.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     const addAddressButton = document.querySelector('.add-address-button');
//     if (addAddressButton) {
//         addAddressButton.addEventListener('click', function(event) {
//             event.preventDefault();
//             window.location.href = 'Add-address.html';
//         }); 
//     }
// });



// Add new card
// document.addEventListener('DOMContentLoaded', function() {
//     const addCardButton = document.querySelector('.add-card-button');

//     if (addCardButton) {
//         addCardButton.addEventListener('click', function() {
//             window.location.href = 'Add-card.html';
//         });
//     }
// });
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const addCard = document.querySelectorAll('.add-card-button');
    addCard.forEach(function(addCard, index) {
        addCard.addEventListener('click', function() {
            const destinationUrl = addCard.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
});



// Save button
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const saveButton = document.querySelectorAll('.save-button');
    saveButton.forEach(function(saveButton, index) {
        saveButton.addEventListener('click', function() {
            const destinationUrl = saveButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     console.log('Document is button');
//     const saveButton = document.querySelectorAll('.save-button');
//     saveButton.forEach(function(saveButton, index) {
//         saveButton.addEventListener('click', function() {
//             const destinationUrl = saveButton.getAttribute('data-url');
//             if (destinationUrl) {
//                 console.log('Navigating to:', destinationUrl); // Check the URL
//                 window.location.href = destinationUrl;
//             }
//         });
//     });
// })

// document.addEventListener('DOMContentLoaded', function() {
//     const saveButton = document.querySelector('.save-button');
//     if (saveButton) {
//         saveButton.addEventListener('click', function(event) {
//             event.preventDefault();
//             const currentPage = getCurrentPageName();
//             if (currentPage === 'Add-card') {
//                 window.location.href = 'Payment-have-card.html';
//             } else if (currentPage === 'Add-address') {
//                 window.location.href = 'Address.html';
//             }
//         });
//     }
// });

function getCurrentPageName() {
    const currentPageUrl = window.location.href;
    const currentPageName = currentPageUrl.substring(currentPageUrl.lastIndexOf('/') + 1).split('.')[0];
    return currentPageName;
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const justifyEnd = document.querySelectorAll('.justify-end');
    justifyEnd.forEach(function(justifyEnd, index) {
        justifyEnd.addEventListener('click', function() {
            const destinationUrl = justifyEnd.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
})

// // Close add-card tab
// document.addEventListener('DOMContentLoaded', function() {
//     const closeButton = document.querySelector('.close-button');

//     if (closeButton) {
//         closeButton.addEventListener('click', function(event) {
//             event.preventDefault();
//             window.location.href = 'Payment-no-card.html';
//         });
//     }
// });



// Pay the order
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const paymentSuccess = document.querySelectorAll('.pay-button');
    paymentSuccess.forEach(function(paymentSuccess, index) {
        paymentSuccess.addEventListener('click', function() {
            const destinationUrl = paymentSuccess.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
})
// document.addEventListener('DOMContentLoaded', function() {
//     const payConfirmButton = document.querySelector('.pay-button');

//     if (payConfirmButton) {
//         payConfirmButton.addEventListener('click', function() {
//             window.location.href = 'Payment-success.html';
//         });
//     }
// });


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
// Log out
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const yesButton = document.querySelectorAll('.yesButton');
    yesButton.forEach(function(yesButton, index) {
        yesButton.addEventListener('click', function() {
            const destinationUrl = yesButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
})

document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const noButton = document.querySelectorAll('.noButton');
    noButton.forEach(function(noButton, index) {
        noButton.addEventListener('click', function() {
            const destinationUrl = noButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
})
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is button');
    const noButton = document.querySelectorAll('.noButton');
    noButton.forEach(function(noButton, index) {
        noButton.addEventListener('click', function() {
            const destinationUrl = noButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    });
})

// Sign up for new Restaurant account
document.addEventListener('DOMContentLoaded', function() {
    console.log('123456')
    const form = document.getElementById('signupForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Form data handling
        const formData = new FormData(form);

        fetch(form.action, { // Assuming your form's 'action' attribute is set to the submission URL
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Handling CSRF token for Django
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle success, such as redirecting to another page or showing a success message
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle errors here, such as displaying an error message to the user
        });
    });
});

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(event) {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            // Simple alert to notify the user what is missing
            alert('Both email and password are required.');
            event.preventDefault(); // Prevent the form from being submitted
        }
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     var orderHistoryButton = document.getElementById('orderHistoryButton');
//     orderHistoryButton.addEventListener('click', function() {
//         window.location.href = '/rorderhistory/';
//     });
// });

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#orderHistoryButton');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    } else {
        console.log('#orderHistoryButton not found');
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#home');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#itemsButton');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#newOrderButton');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#preparingButton');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#readyButton');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#deliveryButton');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.querySelector('#orderTracking');
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const destinationUrl = nextButton.getAttribute('data-url');
            if (destinationUrl) {
                console.log('Navigating to:', destinationUrl); // Check the URL
                window.location.href = destinationUrl;
            }
        });
    }
});