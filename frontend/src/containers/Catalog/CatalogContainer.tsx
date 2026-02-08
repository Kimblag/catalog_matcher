import { useRef, useState, type ChangeEvent } from 'react';
import Upload from '../../components/BulkUpload/Upload';
import DownloadTemplateButton from '../../components/Buttons/DownloadTemplateButton';
import UploadButton from '../../components/Buttons/UploadButton';
import PageHeader from '../../components/Catalog/PageHeader';
import SearchInput from '../../components/Catalog/SearchInput';
import FilterSelect from '../../components/FilterSelect/FilterSelect';
import ItemTableRow from '../../components/ItemTableRow/ItemTableRow';
import { useCatalogData, useCatalogFilters } from '../../hooks';
import CatalogService from '../../services';
import { type ActionState, type CatalogItem } from '../../types';

const CatalogContainer = () => {
  // use ref for upload and for CatalogService
  const uploadAbortRef = useRef<AbortController | null>(null);
  const catalogServiceRef = useRef<CatalogService | null>(null);

  if (!catalogServiceRef.current) {
    catalogServiceRef.current = new CatalogService();
  }
  const {
    catalogItems,
    categories,
    providers,
    includeInactive,
    setCatalogItems,
    setIncludeInactive,
    status,
    subcategories,
  } = useCatalogData(catalogServiceRef.current!);

  const {
    filters: { categoryFilter, providerFilter, searchTerm, subcategoryFilter },
    filteredItems,
    handlers: { clearFilters, handleFilterChange, handleSearchChange },
  } = useCatalogFilters(catalogItems.items);

  const [file, setFile] = useState<File | null>(null);

  // State for action status (uploading, downloading, saving, deleting)
  const [actionState, setActionState] = useState<ActionState>({
    type: 'idle',
  });

  const handleDownloadTemplate = async () => {
    setActionState({ type: 'downloading' });
    const controller = new AbortController();
    try {
      const result = await catalogServiceRef.current!.downloadCatalogTemplate(
        controller.signal,
      );
      if (result.error) {
        setActionState({ type: 'error', error: result.error });
        return;
      }
      const url = window.URL.createObjectURL(result.data!);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'catalog_template.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } finally {
      setActionState({ type: 'idle' });
    }
  };

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement, HTMLInputElement>,
  ) => {
    const selectedFile = event.target.files ? event.target.files[0] : null;
    setFile(selectedFile);
  };

  const handleUploadCSV = async () => {
    if (!file) return;

    setActionState({ type: 'uploading' });

    uploadAbortRef.current?.abort(); // Abort any ongoing upload

    const abortController = new AbortController();
    uploadAbortRef.current = abortController;

    try {
      const uploadResult = await catalogServiceRef.current!.uploadCsv(
        file,
        abortController.signal,
      );

      if (abortController.signal.aborted) {
        return; // If the upload was aborted, exit early without setting error state
      }

      if (uploadResult?.error) {
        setActionState({ type: 'error', error: uploadResult.error });
        return;
      }

      const itemsResult = await catalogServiceRef.current!.getItems(
        abortController.signal,
        includeInactive,
      );
      if (itemsResult.error) {
        setActionState({ type: 'error', error: itemsResult.error });
        return;
      }
      setCatalogItems(itemsResult.data!);
    } finally {
      if (!abortController.signal.aborted) {
        setActionState({ type: 'idle' });
      }
    }
  };

  const handleActivateToggle = async (item: CatalogItem) => {
    const previousItems = structuredClone(catalogItems);

    setCatalogItems((prev) => ({
      items: prev.items.map((i) =>
        i.itemId === item.itemId ? { ...i, active: !i.active } : i,
      ),
    }));

    try {
      setActionState({ type: 'saving', itemId: item.itemId });
      const result = await catalogServiceRef.current!.toggleItemStatus(
        item.itemId,
        !item.active,
      );
      if (result && result.error) {
        setActionState({ type: 'error', error: result.error });
        setCatalogItems(previousItems); // rollback to previous state on error

        return;
      }
    } finally {
      setActionState({ type: 'idle' });
    }
  };

  // Page status handling

  if (status.type === 'loading') {
    return <p>Cargando catálogo...</p>;
  }

  if (status.type === 'error' && status.error) {
    return (
      <div>
        <h2>Error</h2>
        <p>{status.error.message}</p>
      </div>
    );
  }

  return (
    <div>
      <header>
        <PageHeader />
        <DownloadTemplateButton
          onClick={handleDownloadTemplate}
          disabled={actionState.type !== 'idle'}
        />
        {actionState.type === 'uploading' && <p>Subiendo catálogo...</p>}
      </header>

      {/* Upload section */}
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
            onClick={handleUploadCSV}
            disabled={actionState.type !== 'idle' || !file}
          />
          {actionState.type === 'uploading' && <p>Subiendo catálogo...</p>}
        </div>
      </section>
      {/* Table section  */}
      {/* search and filter */}
      <section>
        <SearchInput value={searchTerm} onChange={handleSearchChange} />

        <div>
          <FilterSelect
            name="category"
            onChange={handleFilterChange}
            options={categories}
            value={categoryFilter}
          />
          <FilterSelect
            name="subcategory"
            onChange={handleFilterChange}
            options={subcategories}
            value={subcategoryFilter}
          />
          <FilterSelect
            name="provider"
            onChange={handleFilterChange}
            options={providers}
            value={providerFilter}
          />

          <label>
            <input
              type="checkbox"
              checked={includeInactive}
              onChange={(e) => setIncludeInactive(e.target.checked)}
            />
            Mostrar inactivos
          </label>

          {/* Filter clear */}
          <button type="button" onClick={clearFilters}>
            Limpiar filtros
          </button>
        </div>
      </section>
      <div>
        {actionState.type === 'error' && (
          <div>
            <p>Error: {actionState.error.message}</p>
          </div>
        )}
      </div>
      {/* Table */}
      <div>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Categoría</th>
              <th>Subcategoría</th>
              <th>Descripción</th>
              <th>Unidad</th>
              <th>Proveedor</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filteredItems.length > 0 ? (
              filteredItems.map((item) => (
                <ItemTableRow
                  key={item.itemId}
                  item={item}
                  onActivateToggle={() => handleActivateToggle(item)}
                />
              ))
            ) : (
              <tr>
                <td colSpan={9}>No items found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
export default CatalogContainer;
