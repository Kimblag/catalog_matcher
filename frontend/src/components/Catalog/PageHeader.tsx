import type { PageHeaderProps } from '../../types';

const PageHeader = ({
  title = 'Catálogo de Productos',
  subtitle = 'Gestiona y organiza los productos de tu catálogo de manera eficiente.',
}: PageHeaderProps) => {
  return (
    <>
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </>
  );
};

export default PageHeader;
