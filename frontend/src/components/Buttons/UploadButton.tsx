import type { ButtonProps } from '../../types';

const UploadButton = ({
  label = 'Cargar Archivo',
  onClick,
  disabled = false,
}: ButtonProps) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};

export default UploadButton;
