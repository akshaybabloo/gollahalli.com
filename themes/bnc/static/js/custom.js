const search = instantsearch({
    appId: 'UT1XVMZE1Q',
    apiKey: 'fadcde84f1cdaf165d51c20a50336188',
    indexName: 'gollahalli-website',
    routing: true,
    searchParameters: {
        hitsPerPage: 5
    },
    searchFunction: function (helper) {
        if (helper.state.query === '') {
            if (document.getElementById("hits") != null) {
                document.querySelector('#hits').innerHTML = 'Type to search...';
            }
            if (document.getElementById("hits-sidenav") != null) {
                document.querySelector('#hits-sidenav').innerHTML = 'Type to search...';
            }
            return;
        }
        helper.search();
    }
});

if (document.getElementById("search-input") != null) {
    search.addWidget(
        instantsearch.widgets.searchBox({
            container: '#search-input',
            placeholder: 'Search...',
            magnifier: false,
            reset: false
        })
    );
}

if (document.getElementById("hits") != null) {
    search.addWidget(
        instantsearch.widgets.hits({
            container: '#hits',
            templates: {
                empty: 'No results',
                item: '> <a class="gol-links" href="{{{uri}}}">{{{title}}}</a>'
            },
            escapeHits: true
        })
    );
}

if (document.getElementById("search-input-sidenav") != null) {
    search.addWidget(
        instantsearch.widgets.searchBox({
            container: '#search-input-sidenav',
            placeholder: 'Search...',
            magnifier: false,
            reset: false
        })
    );
}

if (document.getElementById("hits-sidenav") != null) {
    search.addWidget(
        instantsearch.widgets.hits({
            container: '#hits-sidenav',
            templates: {
                empty: 'No results',
                item: '> <a class="gol-links" href="{{{uri}}}">{{{title}}}</a>'
            },
            escapeHits: true
        })
    );
}


search.start();
