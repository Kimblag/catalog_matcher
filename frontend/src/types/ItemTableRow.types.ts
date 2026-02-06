import type { CatalogItem } from './Catalog.types';

export type ItemTableRowProps = {
  item: CatalogItem;
  onActivateToggle?: (itemId: string) => void;
};
