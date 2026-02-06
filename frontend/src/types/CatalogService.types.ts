export type CatalogItemsResponse = {
  items: {
    item_id: string;
    name: string;
    category?: string;
    subcategory?: string;
    description?: string;
    unit?: string;
    provider?: string;
    active: boolean;
    attributes?: Record<string, unknown>;
  }[];
};

export type CatalogCategoriesResponse = {
  categories: Categories;
};

export type CatalogSubcategoriesResponse = {
  subcategories: Subcategories;
};

export type CatalogProvidersResponse = {
  providers: Providers;
};
export type Categories = string[];
export type Subcategories = string[];
export type Providers = string[];
