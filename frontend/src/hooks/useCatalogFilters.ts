/*
    this hook will be used to manage the state of the filters in the catalog page
    it will be used to store the selected filters and to update them when the user interacts with the filter components
    it will also be used to store the available filters and to update them when the user interacts with the filter components
*/

import { useMemo, useState } from 'react';
import type { CatalogItem } from '../types';

export const useCatalogFilters = (items: CatalogItem[]) => {
  // filter state
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string | null>(null);
  const [subcategoryFilter, setSubcategoryFilter] = useState<string | null>(
    null,
  );
  const [providerFilter, setProviderFilter] = useState<string | null>(null);

  // reactive cycle
  // memoized filters to avoid unnecessary computations on every render
  const filteredItems: CatalogItem[] = useMemo(() => {
    return items
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
  }, [items, categoryFilter, subcategoryFilter, providerFilter, searchTerm]);

  /* Actions: Filters handlers */
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const handleFilterChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
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

  const clearFilters = () => {
    setCategoryFilter(null);
    setSubcategoryFilter(null);
    setProviderFilter(null);
    setSearchTerm('');
  };

  return {
    filters: {
      categoryFilter,
      providerFilter,
      searchTerm,
      subcategoryFilter,
    },
    filteredItems,
    handlers: {
      clearFilters,
      handleFilterChange,
      handleSearchChange,
    },
  };
};
