
function storeState() {
    return {
        toggle: {
            men: false,
            women: false,
            kids: false
        },
        setToggle(menu = null) {
            if(menu && menu in this.toggle) this.toggle[menu] = ! this.toggle[menu];
        }
    }
}