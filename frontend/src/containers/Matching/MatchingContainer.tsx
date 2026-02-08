import { useEffect, useRef, useState } from 'react';
import Upload from '../../components/BulkUpload/Upload';
import DownloadTemplateButton from '../../components/Buttons/DownloadTemplateButton';
import UploadButton from '../../components/Buttons/UploadButton';
import PageHeader from '../../components/Catalog/PageHeader';
import InitialCard from '../../components/Matching/InitialCard/InitialCard';
import MatchList from '../../components/Matching/MatchList/MatchList';
import { MatchService } from '../../services/match.service';
import type { ActionState, MatchesList } from '../../types';

const MatchingContainer = () => {
  const [file, setFile] = useState<File | null>(null);

  // State for action status (uploading, downloading, saving, deleting)
  const [actionState, setActionState] = useState<ActionState>({
    type: 'idle',
  });

  // matches state
  const [matches, setMatches] = useState<MatchesList>({ results: [] });

  // Create a reference for the abortcontroller to be used in async operations
  // and to be able to cancel them if the component unmounts or if a new operation starts
  const uploadAbortRef = useRef<AbortController | null>(null);

  // use effect to clean up any ongoing async operations when the component unmounts
  useEffect(() => {
    return () => {
      uploadAbortRef.current?.abort();
    };
  }, []);

  // instance match service only once, it is used in multiple items
  // but not in a initial rendering and it is not a big deal to have it recreated
  const matchService = new MatchService();

  const handleDownloadTemplate = async () => {
    const abortController = new AbortController();

    setActionState({ type: 'downloading' });
    try {
      const result = await matchService.downloadRequirementTemplate(
        abortController.signal,
      );

      // check if there is an error
      if (result.error) {
        setActionState({ type: 'error', error: result.error });
      }

      // build the link
      const url = window.URL.createObjectURL(result.data!);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'requirement_template.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } finally {
      setActionState({ type: 'idle' });
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files ? event.target.files[0] : null;
    setFile(selectedFile);
  };

  const handleUploadCSV = async () => {
    if (!file) return;

    uploadAbortRef.current?.abort(); // cancel any ongoing upload

    //  create a new abort controller for the new upload
    const abortController = new AbortController();
    uploadAbortRef.current = abortController;

    setActionState({ type: 'uploading' });

    try {
      const result = await matchService.uploadCsv(file, abortController.signal);

      // check if it was aborted
      if (abortController.signal.aborted) return;

      if (result.error) {
        setActionState({ type: 'error', error: result.error });
        return;
      }

      setMatches(result.data!);
    } finally {
      if (!abortController.signal.aborted) {
        setActionState({ type: 'idle' });
      }
    }
  };

  return (
    <div>
      {actionState.type === 'error' && (
        <div style={{ color: 'red' }}>
          <p>Error: {actionState.error.message}</p>
        </div>
      )}
      <header>
        <PageHeader
          title="Panel de requerimientos"
          subtitle="Sube el archivo CSV de requerimientos para obtener licitaciones"
        />
        <DownloadTemplateButton
          onClick={handleDownloadTemplate}
          disabled={actionState.type === 'downloading'}
        />
      </header>

      {/* upload section */}
      <section>
        {/* left column */}
        <Upload onFileChange={handleFileChange} />

        {/* right column */}
        <div>
          {/* alert */}
          <article>
            <p>
              Asegúrate de que tu archivo CSV cumpla con la estructura oficial
              de la plantilla.
            </p>
          </article>
          <UploadButton
            label="Ejecutar matching"
            onClick={handleUploadCSV}
            disabled={actionState.type !== 'idle' || !file}
          />
          {actionState.type === 'uploading' && (
            <p>Subiendo requerimientos...</p>
          )}
        </div>
      </section>

      {/* Conditionally render initial state (no matches) */}
      <section>
        {matches.results.length === 0 ? (
          <InitialCard
            uploadButton={
              <UploadButton
                label="Carga tu archivo CSV para empezar"
                onClick={handleUploadCSV}
                disabled={actionState.type !== 'idle' || !file}
              />
            }
          />
        ) : (
          // Render matches
          <MatchList matches={matches} />
        )}
      </section>
    </div>
  );
};

export default MatchingContainer;
