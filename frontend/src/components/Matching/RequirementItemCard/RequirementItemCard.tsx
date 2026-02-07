import type { RequirementItemCardProps } from '../../../types';

const RequirementItemCard = ({
  name,
  description,
  category,
  subcategory,
  unit,
  provider,
}: RequirementItemCardProps) => {
  return (
    <article>
      <div>
        <h3>{name}</h3>
        <p>{description ? description : '-'}</p>
      </div>
      <div>
        {/* 4 columns with requirement details, such as: */}

        <div>
          <h4>Categoría</h4>
          <p>{category ? category : '-'}</p>
        </div>
        <div>
          <h4>Subcategoría</h4>
          <p>{subcategory ? subcategory : '-'}</p>
        </div>
        <div>
          <h4>Unidad</h4>
          <p>{unit ? unit : '-'}</p>
        </div>
        <div>
          <h4>Proveedor</h4>
          <p>{provider ? provider : '-'}</p>
        </div>
      </div>
    </article>
  );
};

export default RequirementItemCard;
