import './main.css';
import Vue from "vue";
import {search, linkedin, times, twitter, github} from "./icons";


new Vue({
    el: '#profile',
    data: {
        linkedin: linkedin.html.pop(),
        github: github.html.pop(),
        twitter: twitter.html.pop(),
        search: search.html.pop(),
        times: times.html.pop(),

        showMenu: true,
        showSearch: true
    },
    methods: {
        showMenuToggle: function () {
            this.showMenu = !this.showMenu;
        },
        showSearchToggle: function () {
            this.showSearch = !this.showSearch;
        }
    }
});

