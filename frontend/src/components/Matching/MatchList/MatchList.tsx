import type { MatchesListProps } from '../../../types';
import RequirementItemCard from '../RequirementItemCard/RequirementItemCard';

const MatchList = ({ matches }: MatchesListProps) => {
  return (
    <>
      {matches.results.map((match) => (
        <div key={match.requirement.name}>
          <RequirementItemCard
            name={match.requirement.name}
            description={match.requirement.description}
            category={match.requirement.category}
            subcategory={match.requirement.subcategory}
            unit={match.requirement.unit}
            provider={match.requirement.provider}
          />
          <table>
            <thead>
              <tr>
                <td>ID</td>
                <td>Nombre</td>
                <td>Descripción</td>
                <td>Categoría</td>
                <td>Subcategoría</td>
                <td>Proveedor</td>
                <td>Score</td>
              </tr>
            </thead>
            <tbody>
              {match.matches.map((item) => (
                <tr key={item.catalogItemId}>
                  <td>{item.catalogItemId}</td>
                  <td>{item.name}</td>
                  <td>{item.description ? item.description : '-'}</td>
                  <td>{item.category ? item.category : '-'}</td>
                  <td>{item.subcategory ? item.subcategory : '-'}</td>
                  <td>{item.provider ? item.provider : '-'}</td>
                  <td>{item.score.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </>
  );
};

export default MatchList;
