import { useEffect, useMemo, useState, type ChangeEvent } from 'react';
import Upload from '../../components/BulkUpload/Upload';
import DownloadTemplateButton from '../../components/Buttons/DownloadTemplateButton';
import UploadButton from '../../components/Buttons/UploadButton';
import PageHeader from '../../components/Catalog/PageHeader';
import SearchInput from '../../components/Catalog/SearchInput';
import FilterSelect from '../../components/FilterSelect/FilterSelect';
import ItemTableRow from '../../components/ItemTableRow/ItemTableRow';
import CatalogService from '../../services';
import {
  type ActionState,
  type CatalogItem,
  type CatalogList,
  type FilterOptions,
  type PageStatus,
} from '../../types';
import { mapToFilterOptions } from '../../utils';

const CatalogContainer = () => {
  const [file, setFile] = useState<File | null>(null);
  const [catalogItems, setCatalogItems] = useState<CatalogList>({ items: [] });

  // filter state
  const [categories, setCategories] = useState<FilterOptions>([]);
  const [subcategories, setSubcategories] = useState<FilterOptions>([]);
  const [providers, setProviders] = useState<FilterOptions>([]);

  const [searchTerm, setSearchTerm] = useState<string>('');

  const [categoryFilter, setCategoryFilter] = useState<string | null>(null);
  const [subcategoryFilter, setSubcategoryFilter] = useState<string | null>(
    null,
  );
  const [providerFilter, setProviderFilter] = useState<string | null>(null);

  const [includeInactive, setIncludeInactive] = useState(false);

  // page status, downloading, uploading, and error states
  const [status, setStatus] = useState<PageStatus>({ type: 'loading' });

  // State for action status (uploading, downloading, saving, deleting)
  const [actionState, setActionState] = useState<ActionState>({
    type: 'idle',
  });

  // Memoized CatalogService to avoid creating a new instance on every render

  const catalogService = useMemo(() => new CatalogService(), []);

  const handleDownloadTemplate = async () => {
    setActionState({ type: 'downloading' });
    const controller = new AbortController();
    try {
      const result = await catalogService.downloadCatalogTemplate(
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
    const controller = new AbortController();
    try {
      const uploadResult = await catalogService.upsertCatalogCSV(
        file,
        controller.signal,
      );

      if (uploadResult?.error) {
        setActionState({ type: 'error', error: uploadResult.error });
        return;
      }

      const itemsResult = await catalogService.getItems(
        controller.signal,
        includeInactive,
      );
      if (itemsResult.error) {
        setActionState({ type: 'error', error: itemsResult.error });
        return;
      }
      setCatalogItems(itemsResult.data!);
    } finally {
      setActionState({ type: 'idle' });
    }
  };

  // use effect to syncronyse with external data source, as the React documentation suggests.
  useEffect(() => {
    const controller = new AbortController();
    const loadInitialData = async () => {
      setStatus({ type: 'loading' });

      const [
        itemsResult,
        categoriesResult,
        subcategoriesResult,
        providersResult,
      ] = await Promise.all([
        catalogService.getItems(controller.signal),
        catalogService.getCategories(controller.signal),
        catalogService.getSubcategories(controller.signal),
        catalogService.getProviders(controller.signal),
      ]);

      const firstError =
        itemsResult.error ||
        categoriesResult.error ||
        subcategoriesResult.error ||
        providersResult.error;

      // If any of the results has an error, set the error state and return early
      if (firstError) {
        setStatus({ type: 'error', error: firstError });
        return;
      }

      setCatalogItems(itemsResult.data!);
      setCategories(
        mapToFilterOptions(categoriesResult.data!, 'Seleccionar categoría'),
      );
      setSubcategories(
        mapToFilterOptions(
          subcategoriesResult.data!,
          'Seleccionar subcategoría',
        ),
      );
      setProviders(
        mapToFilterOptions(providersResult.data!, 'Seleccionar proveedor'),
      );
      setStatus({ type: 'ready' });
    };

    loadInitialData();
  }, [catalogService]);

  // effect dependency to refetch items when includeInactive changes
  useEffect(() => {
    const reloadItems = async () => {
      const controller = new AbortController();
      const result = await catalogService.getItems(
        controller.signal,
        includeInactive,
      );

      if (result.error) {
        return;
      }

      setCatalogItems(result.data!);
    };

    reloadItems();
  }, [includeInactive, catalogService]);

  /* Filters handlers */
  const handleSearchInputChange = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setSearchTerm(event.target.value);
  };

  const handleFilterOnChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    const { name, value } = event.target;
    switch (name) {
      case 'category':
        setCategoryFilter(value);
        break;
      case 'subcategory':
        setSubcategoryFilter(value);
        break;
      case 'provider':
        setProviderFilter(value);
        break;
      default:
        break;
    }
  };

  const handleClearFilters = () => {
    setCategoryFilter(null);
    setSubcategoryFilter(null);
    setProviderFilter(null);
    setSearchTerm('');
  };

  // memoized filters to avoid unnecessary computations on every render
  const filteredItems: CatalogItem[] = useMemo(() => {
    return catalogItems.items
      .filter((item) => !categoryFilter || item.category === categoryFilter)
      .filter(
        (item) => !subcategoryFilter || item.subcategory === subcategoryFilter,
      )
      .filter((item) => !providerFilter || item.provider === providerFilter)
      .filter(
        (item) =>
          item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          item.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
          item.unit?.toLowerCase().includes(searchTerm.toLowerCase()),
      );
  }, [
    catalogItems,
    categoryFilter,
    subcategoryFilter,
    providerFilter,
    searchTerm,
  ]);

  const handleActivateToggle = async (item: CatalogItem) => {
    const previousItems = structuredClone(catalogItems);

    setCatalogItems((prev) => ({
      items: prev.items.map((i) =>
        i.itemId === item.itemId ? { ...i, active: !i.active } : i,
      ),
    }));

    try {
      setActionState({ type: 'saving', itemId: item.itemId });
      const result = await catalogService.toggleItemStatus(
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

        {/* Table section  */}
        {/* search and filter */}
        <section>
          <SearchInput value={searchTerm} onChange={handleSearchInputChange} />

          <div>
            <FilterSelect
              name="category"
              onChange={handleFilterOnChange}
              options={categories}
              value={categoryFilter}
            />
            <FilterSelect
              name="subcategory"
              onChange={handleFilterOnChange}
              options={subcategories}
              value={subcategoryFilter}
            />
            <FilterSelect
              name="provider"
              onChange={handleFilterOnChange}
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
            <button onClick={handleClearFilters}>Clear</button>
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
      </section>
    </div>
  );
};
export default CatalogContainer;
