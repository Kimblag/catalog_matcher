export type PageHeaderProps = {
  title?: string;
  subtitle?: string;
};

export type CatalogItem = {
  itemId: string;
  name: string;
  category?: string;
  subcategory?: string;
  description?: string;
  unit?: string;
  provider?: string;
  active: boolean;
  attributes?: Record<string, unknown>;
};

export type CatalogList = {
  items: CatalogItem[];
};
