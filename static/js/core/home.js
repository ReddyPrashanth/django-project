// purchase plan component state
function purchasePlanState() {
    return {
        selected: 'starter',
        classes: 'max-w-sm w-full border shadow-md rounded mr-2 p-2',
        updateSelection(plan = 'starter') {
            this.selected = plan;
        }
    }   
}

console.log('home.js loaded');