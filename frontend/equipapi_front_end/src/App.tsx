// src/App.tsx
import {useState} from 'react';
import './App.css';
import RetrieveItemsButton from './components/buttons/RetrieveItemsButton';

function App() {
  const [items, setItems] = useState([]);

  const fetchItems = () => {
    fetch('http://localhost:8000/api/rpg/items/?fetch=true')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setItems(data);
      })
      .catch(error => console.error('Error fetching items:', error));
  };

  return (
    <div>
      <h1>Items</h1>
      <RetrieveItemsButton onFetch={fetchItems} />
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name} - {item.itemType} - Stats:
            <ul>
              {Object.entries(item.stats).map(([statName, statValue]) => (
                <li key={statName}>{statName}: {statValue}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;