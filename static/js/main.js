import { initBackground } from './modules/background.js';
import { initReveals } from './modules/reveal.js';
import { initConfirmDialogs } from './modules/confirm.js';

document.addEventListener('DOMContentLoaded', () => {
    initBackground();
    initReveals();
    initConfirmDialogs();
});
