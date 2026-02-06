import { Link } from 'react-router';

const Navbar = () => {
  return (
    <nav>
      <h1>Catalog Matcher</h1>

      <ul>
        <li>
          <Link to="/">Catálogo</Link>
        </li>
        <li>
          <Link to="/matching">Requerimientos</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
