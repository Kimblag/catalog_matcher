import type { FilterOptions } from '../types';

export const mapToFilterOptions = (
  values: string[],
  placeholder: string,
): FilterOptions => {
  return [
    { key: 'all', value: '', label: placeholder },
    ...values.map((value) => ({
      key: value.toLowerCase(),
      value,
      label: value,
    })),
  ];
};
