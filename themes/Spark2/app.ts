import './main.css';
import {icon, library, } from '@fortawesome/fontawesome-svg-core'
import {faGithub, faLinkedin, faTwitter} from '@fortawesome/free-brands-svg-icons';
import {faSearch} from '@fortawesome/free-solid-svg-icons';
import Vue from "vue";


library.add(faGithub, faTwitter, faLinkedin, faSearch);

const linkedin = icon({prefix: 'fab', iconName: 'linkedin'}, {transform: {size: 30}});
const github = icon({prefix: 'fab', iconName: 'github'}, {transform: {size: 30}});
const twitter = icon({prefix: 'fab', iconName: 'twitter'}, {transform: {size: 30}});
const search = icon({prefix: 'fas', iconName: 'search'}, {transform: {size: 20}});

new Vue({
    el: '#profile',
    data: {
        linkedin: linkedin.html.pop(),
        github: github.html.pop(),
        twitter: twitter.html.pop(),
        search: search.html.pop(),
        showMenu: true,
    },
    methods: {
        showMenuToggle: function () {
            this.showMenu = !this.showMenu;
            console.log(this.showMenu);
        }
    }
});
