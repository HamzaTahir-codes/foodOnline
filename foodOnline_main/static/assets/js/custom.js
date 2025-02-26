let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['pk','in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields

    // console.log(place);
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address':address}, function(results, status) {
        // console.log('Results = >>> ', results)
        // console.log('Status = >>>', status)
        if(status == google.maps.GeocoderStatus.OK){
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            console.log(longitude)
            console.log(latitude)

            $('#id_longitude').val(longitude);
            $('#id_latitude').val(latitude);
        }
    });

    //Loop through the address and assign other addresses their values
    console.log(place.address_components);
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){
            //get country
            if(place.address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
            //get State
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            //get City
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }
            //get Pin-Code
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val("");
            }
        }
    }
}

$(document).ready(function(){
    // Add to Cart
    $('.add-to-cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id'); // This will get the id of the foodItem
        url = $(this).attr('data-url'); // This will get the url of the view
        // This will send the food_id to the view
        data = {
            'food_id': food_id,
        }
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            success : function(response){
                console.log(response);
                if (response.status == 'login_required') {
                    Swal.fire({
                        title: 'Login Required',
                        text: 'Please login to continue',
                        icon: 'warning',
                        confirmButtonText: 'OK'
                    }).then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    Swal.fire({
                        title: 'Failed',
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    })
                }else{
                    $('#cart_counter').html(response.counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // Apply amounts
                    applyCartAmount(
                        response.cart_amounts['subtotal'],
                        response.cart_amounts['tax'],
                        response.cart_amounts['grand_total']
                    );
                } 
            }
        })
    })

    $('.item-qty').each(function(){
        var this_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#'+this_id).html(qty);
    })

    // Remove from Cart
    $('.decrease-btn').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id'); // This will get the id of the foodItem
        url = $(this).attr('data-url'); // This will get the url of the view
        item_id = $(this).attr('id');
        // This will send the food_id to the view
        data = {
            'food_id': food_id,
        }
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            success : function(response){
                console.log(response);
                if (response.status == 'login_required'){
                    Swal.fire({
                        title: 'Login Required',
                        text: 'Please login to continue',
                        icon: 'warning',
                        confirmButtonText: 'OK'
                    }).then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    Swal.fire({
                        title: 'Failed',
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    })
                }else{
                    $('#cart_counter').html(response.counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // Apply amounts
                    applyCartAmount(
                        response.cart_amounts['subtotal'],
                        response.cart_amounts['tax'],
                        response.cart_amounts['grand_total']
                    );
                    // Remove cart item when quantity is 0
                    // Did the following because in the marketplace we also got the decrease button, so we want to work it only when it is
                    // on the cart page
                    if(window.location.pathname == '/cart/'){
                        removeCartitem(response.qty, item_id);
                        checkEmptyCart();
                    }
                }   
            }
        })
    });

    // Delete cart item
    $('.delete-cart-item').on('click', function(e){
        e.preventDefault();
        
        item_id = $(this).attr('data-id'); // This will get the id of the Cart Item
        url = $(this).attr('data-url'); // This will get the url of the view
        // This will send the food_id to the view
        data = {
            'item_id': item_id,
        }
        $.ajax({
            type : 'GET',
            url : url,
            data : data,
            success : function(response){
                console.log(response);
                if (response.status == 'login_required'){
                    Swal.fire({
                        title: 'Login Required',
                        text: 'Please login to continue',
                        icon: 'warning',
                        confirmButtonText: 'OK'
                    }).then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    Swal.fire({
                        title: 'Failed',
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    })
                }else{
                    $('#cart_counter').html(response.counter['cart_count']);
                    Swal.fire({
                        title: 'Success',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    })
                    // Apply amounts
                    applyCartAmount(
                        response.cart_amounts['subtotal'],
                        response.cart_amounts['tax'],
                        response.cart_amounts['grand_total']
                    );
                    removeCartitem(0, item_id);
                    checkEmptyCart();
                }   
            }
        })
    });

    // remove cart item when quantity is 0
    function removeCartitem(cartitemQTY, item_id){
        if(cartitemQTY <= 0){
            $('#cart-item-'+item_id).remove();
        }
    }

    //Checks for Empty Cart
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML;
        if (cart_counter == 0){
            document.getElementById('empty-cart').style.display = 'block';
    }}

    function applyCartAmount(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal);
            $('#tax').html(tax);
            $('#grand-total').html(grand_total);
        }
    }
})