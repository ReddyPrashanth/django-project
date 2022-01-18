// Api base URL
const baseURL = 'http://127.0.0.1:8000/blog/api';

// common headers for each api request
const headers = {
    'X-CSRFToken': token
}

// server error message
const SERVER_ERROR = 'Something went wrong. Please try again.'

// replies component state for each post
function repliesState() {
    return {
        replies: [],
        repliesRequested: false,
        show: false,
        count: 0,
        init(count) {
            this.count = parseInt(count);
        },
        fullName(user) {
            return `${user.first_name} ${user.last_name}`;
        },
        toggleReplies(id = null) {
            let event = new CustomEvent("loading");
            if(!this.repliesRequested){
                window.dispatchEvent(event);
                const url = `${baseURL}/comment/${id}/reply`;
                axios.get(url, {headers})
                    .then(response => {
                        this.replies = response.data.replies;
                        window.dispatchEvent(event);
                    }).catch(error => {
                        window.dispatchEvent(event);
                        alert(SERVER_ERROR)
                    });
                this.repliesRequested = true;
            }
            this.show = !this.show;
        },
        addReply($event) {
            if($event.detail) this.replies.unshift($event.detail.reply);
            this.count += 1;
        }
    }
}

// reply modal component state
function replyState() {
    return {
        isOpen: false,
        id: null,
        formData: {
            content: ''
        },
        error: null,
        togglemodal($event = null) {
            if($event) this.id = $event.detail.id;
            this.isOpen = !this.isOpen,
            this.formData.content = '';
            this.error = null;
        },
        saveReply() {
            if(!this.id) alert('Something went wrong. Try again!');
            const data = this.formData;
            const url = `${baseURL}/comment/${this.id}/reply`;
            axios.post(url, data, {headers})
                 .then(response => {
                     const reply = response.data.reply;
                     const event = new CustomEvent('addreply', {detail: { reply: reply}});
                     window.dispatchEvent(event);
                     this.togglemodal()
                 }).catch(error => {
                    this.error = error.response.status === 404 ? 'Comment not found.' : SERVER_ERROR
                 });
        }
    }
}

// post like/dislike component state
function likeState() {
    return {
        like: false,
        dislike: false,
        liked(id = null) {
            if(!this.like && id) {
                const url = `${baseURL}/post/${id}/like`
                axios.get(url, {params: {liked: 1}, headers: headers})
                    .then(response => {
                        this.like = true;
                        this.dislike = false;
                    }).catch(error => {
                        alert(SERVER_ERROR);
                    });
            }
        },
        disliked(id = null) {
            if(!this.dislike && id){
                const url = `${baseURL}/post/${id}/like`
                axios.get(url, {params: {liked: 0}, headers: headers})
                    .then(response => {
                        this.dislike = true;
                        this.like = false;
                    }).catch(error => {
                        alert(SERVER_ERROR);
                    });
            }
        }
    }
}