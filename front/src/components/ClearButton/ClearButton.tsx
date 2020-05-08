import React from 'react';

interface ClearButtonProps {
  onClick: () => void;
  className: string;
}

const ClearButton: React.FC<ClearButtonProps> = (
  {
    onClick = () => {},
    className = '',
  }
) => {
  return (
    <button
      type="button"
      className={`close ${className}`}
      {...{onClick}}
    >
      <span aria-hidden="true">×</span>
    </button>
  );
};

export default ClearButton;
