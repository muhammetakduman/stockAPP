import React, { useState } from 'react';
import ProductForm from './components/ProductForm';
import ProductList from './components/ProductList';
import { Container, Typography } from '@mui/material';

function App() {
  const [refresh, setRefresh] = useState(false);

  const handleProductAdded = () => {
    setRefresh(!refresh);
  };

  return (
    <Container sx={{ marginTop: '50px', display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
      <div><Typography variant="h4" align="center" gutterBottom>Stok Yönetim Sistemi</Typography>
        <ProductForm onProductAdded={handleProductAdded} /></div>
      <div><ProductList key={refresh} /></div>

    </Container>
  );
}

export default App;
