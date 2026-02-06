import type { ButtonProps } from '../../types';

const DownloadTemplateButton = ({
  label = 'Descargar Plantilla',
  onClick,
  disabled = false,
}: ButtonProps) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};

export default DownloadTemplateButton;
