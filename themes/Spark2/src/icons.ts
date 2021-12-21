import {icon, library, } from '@fortawesome/fontawesome-svg-core'
import {faGithub, faLinkedin, faTwitter} from '@fortawesome/free-brands-svg-icons';
import {faSearch, faTimes, faHashtag} from '@fortawesome/free-solid-svg-icons';

library.add(faGithub, faTwitter, faLinkedin, faSearch, faTimes, faHashtag);

export const linkedin = icon({prefix: 'fab', iconName: 'linkedin'}, {transform: {size: 30}});
export const github = icon({prefix: 'fab', iconName: 'github'}, {transform: {size: 30}});
export const twitter = icon({prefix: 'fab', iconName: 'twitter'}, {transform: {size: 30}});
export const search = icon({prefix: 'fas', iconName: 'search'}, {transform: {size: 20}});
export const times = icon({prefix: 'fas', iconName: 'times'}, {transform: {size: 20}});
export const hashTag = icon({prefix: 'fas', iconName: 'hashtag'});