
function cartQuantity() {
    return {
        total_products: 0,
        init() {
            axios.get('http://127.0.0.1:8000/cart/total-products/', {headers})
                .then(response => {
                    this.total_products = response.data.total_products;
                }).catch(error => console.error(error))
        },
        updateCart($event) {
            if($event.detail) this.total_products = $event.detail;
        }
    }
}