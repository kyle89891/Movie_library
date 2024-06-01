new Vue({
    el: '#app',
    data: {
        query: '',
        searchResults: [],
        movieLists: [],
        newListName: '',
        newListIsPublic: false,
    },
    methods: {
        searchMovies() {
            fetch(`/api/search/?q=${this.query}`)
                .then(response => response.json())
                .then(data => this.searchResults = data.Search);
        },
        fetchMovieLists() {
            fetch('/api/lists/')
                .then(response => response.json())
                .then(data => this.movieLists = data);
        },
        createMovieList() {
            fetch('/api/lists/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    name: this.newListName,
                    is_public: this.newListIsPublic
                })
            }).then(response => {
                if (response.ok) {
                    this.fetchMovieLists();
                    this.newListName = '';
                    this.newListIsPublic = false;
                }
            });
        }
    },
    created() {
        this.fetchMovieLists();
    }
});
