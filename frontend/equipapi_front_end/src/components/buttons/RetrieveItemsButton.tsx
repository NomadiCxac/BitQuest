// src/components/buttons/RetrieveItemsButton.tsx
import React from 'react';

interface Props {
  onFetch: () => void;  // Prop to handle the click event
}

const RetrieveItemsButton: React.FC<Props> = ({ onFetch }) => {
  return (
    <button onClick={onFetch}>Fetch Items</button>
  );
};

export default RetrieveItemsButton;