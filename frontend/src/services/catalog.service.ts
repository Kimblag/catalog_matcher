import type {
  ApiError,
  CatalogCategoriesResponse,
  CatalogItem,
  CatalogItemsResponse,
  CatalogList,
  CatalogProvidersResponse,
  CatalogSubcategoriesResponse,
  Categories,
  Providers,
  Subcategories,
} from '../types';
import HttpClient from './httpClient';

export class CatalogService {
  // Download catalog template
  async downloadCatalogTemplate(
    signal?: AbortSignal,
  ): Promise<{ data?: Blob; error?: ApiError }> {
    const client = new HttpClient('/api/templates/catalogs', 'blob');

    // check if there is an error in the response
    const response = await client.request<Blob>(signal);
    if (response.error) {
      return { error: response.error };
    }

    if (!response.data) {
      return {
        error: {
          code: 'invalid_response',
          message: 'Invalid response format: missing data',
        },
      };
    }
    return { data: response.data };
  }

  // Upload catalog CSV
  async upsertCatalogCSV(
    file: File,
    signal?: AbortSignal,
  ): Promise<{ error?: ApiError } | void> {
    const formData = new FormData();
    formData.append('catalog_file', file);

    const client = new HttpClient('/api/catalog/items', undefined, {
      method: 'POST',
      body: formData,
    });

    const response = await client.request<void>(signal);
    if (response.error) {
      return { error: response.error };
    }
    return;
  }

  // Get catalog items
  async getItems(
    signal?: AbortSignal,
    includeInactive: boolean = false,
  ): Promise<{ data?: CatalogList; error?: ApiError }> {
    const client = new HttpClient(
      `/api/catalog?include_inactive=${includeInactive}`,
      'json',
    );
    const response = await client.request<CatalogItemsResponse>(signal);

    //  check if there is an error in the response
    if (response.error) return { error: response.error };

    // check if there are items in the response
    if (!response.data?.items) {
      return {
        error: {
          code: 'invalid_response',
          message: 'Invalid response format: missing items',
        },
      };
    }

    // map item_id to itemId for each item in the response
    const items: CatalogItem[] = response.data.items.map((item) => ({
      itemId: item.item_id,
      name: item.name,
      category: item.category,
      subcategory: item.subcategory,
      description: item.description,
      unit: item.unit,
      provider: item.provider,
      active: item.active,
      attributes: item.attributes,
    }));

    // Return type catalogList promise with items
    return { data: { items } };
  }

  // list categories
  async getCategories(
    signal?: AbortSignal,
  ): Promise<{ data?: Categories; error?: ApiError }> {
    const client = new HttpClient('/api/catalog/categories', 'json');
    const response = await client.request<CatalogCategoriesResponse>(signal);

    // check if there is an error in the response
    if (response.error) return { error: response.error };

    if (!response || !response.data?.categories) {
      return {
        error: {
          code: 'invalid_response',
          message: 'Invalid response format',
        },
      };
    }

    return { data: response.data.categories };
  }

  // list subcategories
  async getSubcategories(signal?: AbortSignal): Promise<{
    data?: Subcategories;
    error?: ApiError;
  }> {
    const client = new HttpClient('/api/catalog/subcategories', 'json');
    const response = await client.request<CatalogSubcategoriesResponse>(signal);

    // check error in response
    if (response.error) return { error: response.error };

    if (!response || !response.data?.subcategories) {
      return {
        error: {
          code: 'invalid_response',
          message: 'Invalid response format',
        },
      };
    }

    return { data: response.data.subcategories };
  }

  // list providers
  async getProviders(
    signal?: AbortSignal,
  ): Promise<{ data?: Providers; error?: ApiError }> {
    const client = new HttpClient('/api/catalog/providers', 'json');
    const response = await client.request<CatalogProvidersResponse>(signal);

    // check error in response
    if (response.error) return { error: response.error };

    if (!response || !response.data?.providers) {
      return {
        error: {
          code: 'invalid_response',
          message: 'Invalid response format',
        },
      };
    }

    return { data: response.data.providers };
  }

  // deactivate or activate item
  async toggleItemStatus(
    itemId: string,
    status: boolean,
    signal?: AbortSignal,
  ): Promise<{ error?: ApiError } | void> {
    const client = new HttpClient(
      `/api/catalog/items/${itemId}/status`,
      undefined,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ active: status }),
      },
    );

    const response = await client.request<void>(signal);
    if (response.error) {
      return { error: response.error };
    }
    return;
  }
}
