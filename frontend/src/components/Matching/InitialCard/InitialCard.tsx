import type { InitialCardProps } from '../../../types';

const InitialCard = ({ uploadButton }: InitialCardProps) => {
  return (
    <div>
      <h2>Bienvenido al panel de requerimientos</h2>

      {/* here goes an Icon placeholder */}

      <h3>Inicia el matching de tus requerimientos</h3>
      <p>
        Carga el archivo CSV de requerimientos para comenzar a obtener los
        resultados de licitaciones correspondientes. Nuestro algoritmo
        automáticamente analizará tus requerimientos y los comparará con nuestro
        catálogo de licitaciones para encontrar las mejores coincidencias.
        Asegúrate de que tu archivo CSV cumpla con la estructura oficial de la
        plantilla para garantizar resultados precisos.
      </p>

      {/* Call to action to upload a CSV (is the same button as the upload) */}
      {uploadButton}
      <p>Extensiones soportadas: .CSV</p>
    </div>
  );
};

export default InitialCard;
