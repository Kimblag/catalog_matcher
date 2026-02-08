import { useEffect, useState } from 'react';
import type { CatalogList, FilterOptions, PageStatus } from '../types';
import type CatalogService from '../services';
import { mapToFilterOptions } from '../utils';

export const useCatalogData = (service: CatalogService) => {
  const [catalogItems, setCatalogItems] = useState<CatalogList>({ items: [] });

  // filter state
  const [categories, setCategories] = useState<FilterOptions>([]);
  const [subcategories, setSubcategories] = useState<FilterOptions>([]);
  const [providers, setProviders] = useState<FilterOptions>([]);
  const [includeInactive, setIncludeInactive] = useState(false);

  // page status, downloading, uploading, and error states
  const [status, setStatus] = useState<PageStatus>({ type: 'loading' });

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
        service.getItems(controller.signal),
        service.getCategories(controller.signal),
        service.getSubcategories(controller.signal),
        service.getProviders(controller.signal),
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

    return () => {
      controller.abort(); // Cleanup on unmount
    };
  }, []); // do not pass the service dependency,
  // because is not expected to change during the lifecycle of the component,
  // we are using useRef in the CatalogContainer to ensure that the same instance is used across renders.

  // effect dependency to refetch items when includeInactive changes
  useEffect(() => {
    const controller = new AbortController();

    const reloadItems = async () => {
      const result = await service.getItems(controller.signal, includeInactive);

      if (result.error) {
        return;
      }

      setCatalogItems(result.data!);
    };

    reloadItems();

    return () => {
      controller.abort();
    };
  }, [includeInactive]);

  return {
    catalogItems,
    categories,
    providers,
    setCatalogItems,
    status,
    subcategories,
    includeInactive,
    setIncludeInactive,
  };
};
