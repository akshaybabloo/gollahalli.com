import './main.css';
import Vue from "vue";
import {search, linkedin, times, twitter, github} from "./icons";
import algoliasearch from "algoliasearch/lite";
import {groupBy} from "lodash";


// @ts-ignore
const client = algoliasearch(algoliaAppId, algoliaApiKey);
// @ts-ignore
const index = client.initIndex(algoliaIndexName);

new Vue({
    el: '#profile',
    data: {
        linkedin: linkedin.html.pop(),
        github: github.html.pop(),
        twitter: twitter.html.pop(),
        search: search.html.pop(),
        times: times.html.pop(),
        searchText: "",
        hits: [],
        numberOfHits: 0,

        showMenu: true,
        showSearch: true
    },
    methods: {
        showMenuToggle: function () {
            this.showMenu = !this.showMenu;
        },
        showSearchToggle: function () {
            this.showSearch = !this.showSearch;
        },
        searchAlgolia: function (event: HTMLInputElement) {
            if (this.searchText === "") {
                this.numberOfHits = 0;
                this.hits = [];
                return;
            }
            index.search(this.searchText).then(value => {
                this.numberOfHits = value.nbHits;
                // @ts-ignore
                this.hits = groupBy(value.hits, "section");
                console.log(this.hits);
            }).catch(reason => {
                console.error(reason);
            })
        }
    }
});
