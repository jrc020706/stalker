import { Home } from '../views/Home.js';
import { Services } from '../views/Services.js';
import { Contact } from '../views/Contact.js';
import { render } from '../app.js';

export function router() {
  const route = location.hash;

  switch (route) {
    case "#/home":
      render(Home());
      break;
    case "#/services":
      render(Services());
      break;
    case "#/contact":
      render(Contact());
      break;
    default:
      render(Home());
  }
}