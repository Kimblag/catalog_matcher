import type { ChangeEvent } from 'react';

export type FilterSelectProps = {
  name: string;
  value: string | null;
  options: FilterOptions;
  onChange: (event: ChangeEvent<HTMLSelectElement>) => void;
};

export type FilterOptions = {
  key: string;
  value: string | null;
  label: string;
}[];
