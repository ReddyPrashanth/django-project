const CART_URL = 'http://127.0.0.1:8000/cart/add'

function sizeSelection() {
    return {
        data: {
            size: {
                value: null,
                error: null
            },
            color: {
                value: null,
                error: null
            },
            product_id: null
        },
        bgColor: 'bg-black',
        textColor: 'text-white',
        borderColor: 'border-black',
        borderSize: 'border-2',
        isOpen: false,
        toggleModal() {
            this.isOpen = !this.isOpen
        },
        init(product_id) {
            if(product_id) this.data.product_id = product_id
        },
        onSizeSelect(el, size=null) {
            [...el.parentElement.children].forEach(sib => sib.classList.remove(this.bgColor, this.textColor));
            el.classList.add(this.bgColor, this.textColor);
            this.data.size.value = size;
            if(this.data.size.error) this.data.size.error = null;
        },
        onColorSelect(el, color=null, inventory = null) {
            [...el.parentElement.children].forEach(sib => sib.classList.remove(this.borderColor, this.borderSize));
            el.classList.add(this.borderColor, this.borderSize);
            this.data.color.value = color;
            if(this.data.color.error) this.data.color.error = null;
        },
        addToCart() {
            if(!this.data.size.value) {
                this.data.size.error = 'Please select your size';
                return;
            }
            if(!this.data.color.value) {
                this.data.color.error = 'Please select your color';
                return;
            }
            product_id = this.data.product_id;
            if(product_id) {
                axios.post(`${CART_URL}/${product_id}`, {quantity: 1, update:false}, {headers})
                .then(response => {
                    total_products = response.data.total_products;
                    this.data.size.value = null;
                    this.data.color.value = null;
                    const sizeEl = document.getElementById('sizes');
                    const colorEl = document.getElementById('colors');
                    const cartEvent = new CustomEvent("updatecart", {detail: total_products})
                    window.dispatchEvent(cartEvent);
                    const event = new CustomEvent("toggle");
                    window.dispatchEvent(event);
                    [...sizeEl.children].forEach(sib => sib.classList.remove(this.bgColor, this.textColor));
                    [...colorEl.children].forEach(sib => sib.classList.remove(this.borderColor, this.borderSize));
                }).catch(error => console.log(error.response.data))
            }
        }
    }
}