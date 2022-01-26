console.log('products.js loaded');

function sizeFilterState() {
    return {
        onSizeSelect(size = null) {
            if(!size) return;
            const href = window.location.href;
            const [url, queryString] = href.split('?');
            let queryObj = {}
            if(queryString){
                const queryParams = queryString.split('&');
                queryObj = queryParams.reduce((accum, curr) => {
                    const [key, value] = curr.split('=');
                    accum[key] = value;
                    return accum;
                }, {});
            }
            queryObj['size'] = size;
            queryObj['page'] = 1;
            const keys = Object.keys(queryObj);
            const qryStr = keys.reduce((accum, curr, index) => {
                accum += index === keys.length -1 ? `${curr}=${queryObj[curr]}`: `${curr}=${queryObj[curr]}&`;
                return accum;
            },'');
            window.location.href = `${url}?${qryStr}`;
        }
    }
}