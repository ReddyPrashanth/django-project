console.log('Checkout.js loaded');
let address;
let autocomplete;
let form = document.getElementById('address-form');
let phoneEl;
function initAutocomplete() {
    address = form.querySelector('#address');
    phoneEl = form.querySelector('#phone');
    autocomplete = new google.maps.places.Autocomplete(address, {
        componentRestrictions: {country: ["us"]},
        fields: ["address_components", "geometry"],
        types: ["address"]
    });
    autocomplete.addListener("place_changed", fillInAddress);
}

function fillInAddress() {
    const place = autocomplete.getPlace();
    let address = '';
    const event = new Event('input');
    for (const component of place.address_components) {
        const componentType = component.types[0];
        switch (componentType) {
          case "street_number":
            address = `${component.long_name} ${address}`;
            break;
          case "route":
            address += component.long_name;
            break;
          case "postal_code":
            const zipcode = component.long_name;
            const zipcodeEl = form.querySelector('#zipcode');
            zipcodeEl.value = zipcode;
            zipcodeEl.dispatchEvent(event);
            break;
          case "locality":
            const city = component.long_name;
            const cityEl = form.querySelector('#city');
            cityEl.value = city;
            cityEl.dispatchEvent(event);
            break;
          case "administrative_area_level_1":
            const state = component.long_name;
            const stateEl = form.querySelector('#state');
            stateEl.value = state;
            stateEl.dispatchEvent(event);
            break;
        }
    }
    const addressEl = form.querySelector('#address');
    addressEl.value = address;
    form.dispatchEvent(new CustomEvent('addressevent', {detail: address}))
    phoneEl.focus();
}

function addressState() {
    return {
        data: {
            last_name: '',
            first_name: '',
            email: '',
            address: '',
            phone: '',
            city: '',
            state: '',
            zipcode: ''
        },
        selected: false,
        submitForm() {
            this.selected = !this.selected;
        },
        setAddress(event) {
            this.data.address = event.detail;
        }
    }
}

