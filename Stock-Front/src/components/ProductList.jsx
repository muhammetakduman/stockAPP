import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Typography, List, ListItem, ListItemText } from '@mui/material';

function ProductList() {
    const [products, setProducts] = useState([]);

    const fetchProducts = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/products');
            setProducts(response.data.products);
        } catch (error) {
            console.error("Ürünler alınırken hata oluştu:", error);
        }
    };

    useEffect(() => {
        fetchProducts();
    }, []);

    return (
        <Container maxWidth="sm">
            <Typography variant="h5" gutterBottom>Ürün Listesi</Typography>
            <List>
                {products.map((product) => (
                    <ListItem key={product.id}>
                        <ListItemText
                            primary={product.name}
                            secondary={`Açıklama: ${product.description}, Fiyat: ${product.unit_price}, Stok: ${product.stock}`}
                        />
                    </ListItem>
                ))}
            </List>
        </Container>
    );
}

export default ProductList;
