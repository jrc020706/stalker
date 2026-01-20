const app = document.getElementById('app');

export function render(view) {
   
  app.innerHTML = `<main>${view}</main>`;
}