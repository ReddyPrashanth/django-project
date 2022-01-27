console.log('products.js loaded');

function buildQueryObject() {
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
    return {url, queryObj};
}

function buildQueryString(queryObj = {}) {
    const keys = Object.keys(queryObj);
    const qryStr = keys.reduce((accum, curr, index) => {
        accum += index === keys.length -1 ? `${curr}=${queryObj[curr]}`: `${curr}=${queryObj[curr]}&`;
        return accum;
    },'');
    return qryStr
}

function sizeFilterState() {
    return {
        onSizeSelect(size = null) {
            if(!size) return;
            const {url, queryObj} = buildQueryObject();
            queryObj['size'] = size;
            queryObj['page'] = 1;
            const qryStr = buildQueryString(queryObj);
            window.location.href = qryStr.length > 0 ? `${url}?${qryStr}`: url;
        }
    }
}

function clearFilterState() {
    return {
        removeFilter(filter=null) {
            console.log(filter);
            if(filter) {
                const {url, queryObj} = buildQueryObject();
                const min_price = 'min_price';
                const max_price = 'max_price';
                if(filter in queryObj) {
                    if(filter === min_price || filter === max_price){
                        delete queryObj[min_price];
                        delete queryObj[max_price];
                        console.log(queryObj);
                    } else delete queryObj[filter];
                }
                const qryStr = buildQueryString(queryObj);
                window.location.href = qryStr.length > 0 ? `${url}?${qryStr}`: url;
            }
        }
    }
}