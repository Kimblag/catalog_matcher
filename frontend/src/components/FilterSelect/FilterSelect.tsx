import type { FilterSelectProps } from '../../types';

const FilterSelect = ({
  name,
  value,
  options,
  onChange,
}: FilterSelectProps) => {
  return (
    <>
      <select
        name={name}
        id={name}
        value={value || ''} // Ensure value is never undefined
        onChange={(event: React.ChangeEvent<HTMLSelectElement>) =>
          onChange(event)
        }
      >
        {options.map((option) => (
          <option key={option.key} value={option.value || ''}>
            {option.label}
          </option>
        ))}
      </select>
    </>
  );
};

export default FilterSelect;
