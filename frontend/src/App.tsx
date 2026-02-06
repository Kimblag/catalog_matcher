import { Route, Routes } from 'react-router';
import Layout from './containers/Layout/Layout';
import MatchingContainer from './containers/Matching/MatchingContainer';
import CatalogContainer from './containers/Catalog/CatalogContainer';

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={<Layout />}
        children={[
          <Route index element={<CatalogContainer />} />,
          <Route path="matching" element={<MatchingContainer />} />,
        ]}
      />
    </Routes>
  );
}

export default App;
