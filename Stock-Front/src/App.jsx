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
    <Container>
      <Typography variant="h4" align="center" gutterBottom>Stok Yönetim Sistemi</Typography>
      <ProductForm onProductAdded={handleProductAdded} />
      <ProductList key={refresh} />
    </Container>
  );
}

export default App;
