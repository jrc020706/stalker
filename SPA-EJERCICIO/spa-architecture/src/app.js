import { Navbar } from './components/Navbar.js';
import { router } from './router/router.js';

const app = document.getElementById('app');

export function render(view) {
    console.log(document.getElementById("app"));
    app.innerHTML = `
    ${Navbar()}
    <main>${view}</main>
  `;
}

window.addEventListener('hashchange', router);
window.addEventListener('load', router);