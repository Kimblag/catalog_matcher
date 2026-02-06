import type { SearchInputProps } from '../../types';

const SearchInput = ({ value, onChange }: SearchInputProps) => {
  return (
    <form>
      <input
        id="search"
        name="search"
        placeholder="Buscar..."
        onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
          onChange(event)
        }
        type="search"
        value={value}
      />
    </form>
  );
};

export default SearchInput;
