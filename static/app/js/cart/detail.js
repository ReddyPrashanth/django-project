
const CART_URL = 'http://127.0.0.1:8000/cart/add'

function cartState() {
    return {
        data: {
            sub_total: 0,
            tax: 0,
            total: 0
        },
        init(data = null){
            if(data) {
                this.data.sub_total = data.sub_total;
                this.data.tax = data.tax;
                this.data.total = data.total
            }
        },
        updateProductQuantity(event, product_id = null) {
            const el = event.target.getElementsByClassName('item_price')[0];
            const quantity = parseInt(event.target.elements['quantity'].value);
            if(product_id && !isNaN(quantity)) {
                axios.post(`${CART_URL}/${product_id}`, {quantity, update:true}, {headers})
                .then(response => {
                    const {total_products, item_total_price, tax, sub_total, total} = response.data;
                    this.init({sub_total, tax, total});
                    el.innerText = `$${item_total_price}`;
                    const event = new CustomEvent('updatecart', {detail: total_products});
                    window.dispatchEvent(event);
                    alert('Cart updated successfully.');
                }).catch(error => {
                    console.log(error)
                    alert("Something went wrong. Can't update quantity");
                })
            }
        }
    }
}