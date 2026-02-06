import { Outlet } from 'react-router';
import Navbar from '../../components/Layout/Navbar';

const Layout = () => {
  return (
    <div>
      <Navbar />

      <main>
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
