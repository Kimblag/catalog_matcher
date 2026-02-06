import type { ItemTableRowProps } from '../../types';

const ItemTableRow = ({ item, onActivateToggle }: ItemTableRowProps) => {
  return (
    <tr>
      {/* loop through item properties */}
      {Object.entries(item).map(([key, value]) =>
        // if key is attributes, continue to next iteration
        key === 'attributes' ? null : <td key={key}>{String(value)}</td>,
      )}
      <td>
        <label>
          <input
            type="checkbox"
            checked={item.active}
            onChange={() => onActivateToggle && onActivateToggle(item.itemId)}
          />
          <span></span>
        </label>
      </td>
    </tr>
  );
};

export default ItemTableRow;
